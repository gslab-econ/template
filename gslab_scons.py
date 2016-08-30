'''
#################################################################
#  gslab_scons.py - Help/Documentation for gslab_scons.py       #
#################################################################

# Description:
gslab_scons.py is a Python module containing functions used in GSLab's recommended Scons repo template.

# Usage:

## Pre-requisites
- OS supported: Windows (`cmd`), Mac OS, Linux OS
- Stata: Support for Stata-MP, Stata-SE, and Stata. Executable should be added to the `PATH` environment and callable from command line. 
- R: executable should be added to the `PATH` environment so that it is callable from command line with `R`.
- scons
- Lyx: executable should be added to the `PATH` environment so that it is callable from command line with `lyx`.

## Setup
In setting up GSLab's repo Scons template, SConstruct requires this module to supply its builders with specific
executable and commands. 
The location of executables for R, Stata, and Lyx must first be added to the PATH environment.
Top-directory SConstruct file should include:
```
import gslab_scons
```
Builders are setup using Scons' default format for builder and added to Scons' environment dictionary.
SConscript files can then call the builder through the environment dictionary, e.g. `env.Stata`.

When calling builders from SConscript, the source code file (e.g. `.do` for Stata) must be listed as the first argument in source.

## Run
 - The entire directory:
    - In the root directory, type `scons`. This should run everything that is flagged as being modified or with dependencies that have been modified.
 - A single directory of targets:
    - `scons output/data` will re-build the `output/data` folder if it is out of sync, without rebuilding other files.
 - A single target file:
    - `scons output/paper/paper.pdf` will re-run only the code needed to update `output/paper/paper.pdf` without rebuilding other files.

User can specify flavour by typing `scons --sf=StataMP` (default: Scons will try to find each flavour).
'''

import os, sys, shutil, subprocess
from datetime import datetime
from sys import platform
from gslab_fill.tablefill import tablefill

def start_log(log = 'sconstruct.log'):
    if is_unix():
        sys.stdout = os.popen('tee %s' % log, 'w')
    elif platform == 'win32':
        sys.stdout = open(log, 'w')
    now = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    sys.stdout.write( now + '\n')
    sys.stderr = sys.stdout 
    return None

def build_tables(target, source, env):
    tablefill(input    = ' '.join(env.GetBuildPath(env['INPUTS'])), 
              template = env.GetBuildPath(source[0]), 
              output   = env.GetBuildPath(target[0]))
    return None

def build_lyx(target, source, env):
    source_file = str(source[0])
    target_file = str(target[0])
    target_dir  = os.path.dirname(target_file)
    check_source_code_extension(source_file, 'lyx')
    newpdf      = source_file.replace('.lyx','.pdf')
    
    log_file    = target_dir + '/sconscript.log'
    silent_remove(log_file)
    
    os.system('lyx -e pdf2 %s > %s' % (source_file, log_file))
    
    shutil.move(newpdf, target_file)
    time_prepender(log_file)
    return None

def build_r(target, source, env):
    source_file = str(source[0])
    target_file = str(target[0])
    target_dir  = os.path.dirname(target_file)
    check_source_code_extension(source_file, 'r')

    log_file    = target_dir + '/sconscript.log'
    silent_remove(log_file)

    os.system('R CMD BATCH --no-save %s %s' % (source_file, log_file))
    
    time_prepender(log_file)
    return None

def build_stata(target, source, env):
    source_file  = str(source[0])
    target_file  = str(target[0])
    target_dir   = os.path.dirname(target_file)
    check_source_code_extension(source_file, 'stata')

    log_file = target_dir + '/sconscript.log'
    silent_remove(log_file)
    loc_log  = os.path.basename(source_file).replace('.do','.log')

    user_flavor  = env['user_flavor']  
    if user_flavor is not None:
        if is_unix():
            command = stata_command_unix(user_flavor)
        elif platform == 'win32':
            command = stata_command_win(user_flavor)
    else:
        flavors = ['stata-mp', 'stata-se', 'stata']
        if is_unix():
            for flavor in flavors:
                if is_in_path(flavor):
                    command = stata_command_unix(flavor)
                    break
        elif platform == 'win32':
            try:
                key_exist = os.environ['STATAEXE'] is not None
                command = stata_command_win("%%STATAEXE%%")
            except KeyError:
                flavors = [(f.replace('-', '') + '.exe') for f in flavors]
                if is_64_windows():
                    flavors = [f.replace('.exe', '-64.exe') for f in flavors]
                for flavor in flavors:
                    if is_in_path(flavor):
                        command = stata_command_win(flavor)
                        break
    try:
        subprocess.check_output(command % source_file, shell = True)
    except subprocess.CalledProcessError:
        print('*** Error: Cannot find Stata executable.')

    shutil.move(loc_log, log_file)
    time_prepender(log_file)
    return None

def stata_command_unix(flavor):
    options = {'darwin': '-e',
               'linux' : '-b',
               'linux2': '-b'}
    option  = options[platform]
    command = flavor + ' ' + option + ' %s '
    return command

def stata_command_win(flavor):
    command  = flavor + ' /e do' + ' %s '
    return command

def is_unix():
    unix = ['darwin', 'linux', 'linux2']
    return platform in unix

def is_64_windows():
    return 'PROGRAMFILES(X86)' in os.environ

def silent_remove(filename):
    try:
        os.remove(filename)
    except OSError:
        pass
    return None

def is_in_path(program):
    # General helper function to check if `program` exist in the path env
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ['PATH'].split(os.pathsep):
            path = path.strip("'")
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None

def time_prepender(filename):
    now = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    with open(filename, mode = 'r+U') as f:
        content = f.read()
        f.seek(0, 0)
        f.write('Log created at ' + now + '\n \n' + content)
    return None

def check_source_code_extension(source_file, software):
    extensions = {'stata': '.do',
                  'r'    : '.r', 
                  'lyx'  : '.lyx'}
    ext = extensions[software]
    source_file = str.lower(source_file)
    if not source_file.endswith(ext):
        try:
            raise ValueError()
        except ValueError:
            print('*** Error: ' + 'First argument in `source`, ' + source_file + ', must be a ' + ext + ' file')    
    return None
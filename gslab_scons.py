'''
#################################################################
#  gslab_scons.py - Help/Documentation for gslab_scons.py       #
#################################################################

# Description:
gslab_scons.py is a Python module containing general-purpose Scons builders for Lyx, 
R, and Stata.

OS supported: Windows (`cmd`), Mac OS, Linux OS
Prerequisite: scons 

When calling builders from SConscript, the source code file (e.g. `.do` for Stata) 
must be listed as the first argument in source.
'''

import os, sys, shutil, subprocess
from datetime import datetime
from sys import platform
from gslab_fill.tablefill import tablefill

def start_log(log = 'sconstruct.log'):
    check_lfs()
    if is_unix():
        sys.stdout = os.popen('tee %s' % log, 'w')
    elif platform == 'win32':
        sys.stdout = open(log, 'w')
    sys.stderr = sys.stdout 
    return None

def check_lfs():
    try:
        output = subprocess.check_output("git-lfs install", shell = True)
    except:
        try:
            output = subprocess.check_output("git-lfs init", shell = True) # init is deprecated version of install
        except:
            sys.exit('''ERROR: Either Git LFS is not installed or your Git LFS settings need to be updated. 
                  Please install Git LFS or run 'git lfs install --force' if prompted above.''')


def build_tables(target, source, env):
    tablefill(input    = ' '.join(env.GetBuildPath(env['INPUTS'])), 
              template = env.GetBuildPath(source[0]), 
              output   = env.GetBuildPath(target[0]))
    return None

def build_lyx(target, source, env):
    start_time  = current_time()
    source_file = str(source[0])
    target_file = str(target[0])
    target_dir  = os.path.dirname(target_file)
    check_source_code_extension(source_file, 'lyx')
    newpdf      = source_file.replace('.lyx','.pdf')
    log_file    = target_dir + '/sconscript.log'
    
    os.system('lyx -e pdf2 %s > %s' % (source_file, log_file))
    
    shutil.move(newpdf, target_file)
    end_time    = current_time()
    log_timestamp(start_time, end_time, log_file)
    return None

def build_r(target, source, env):
    start_time  = current_time()
    source_file = str(source[0])
    target_file = str(target[0])
    target_dir  = os.path.dirname(target_file)
    check_source_code_extension(source_file, 'r')
    log_file    = target_dir + '/sconscript.log'

    os.system('R CMD BATCH --no-save %s %s' % (source_file, log_file))

    end_time   =  current_time()    
    log_timestamp(start_time, end_time, log_file)
    return None

def build_stata(target, source, env):
    ''' User can specify flavour by typing `scons sf=StataMP` 
       (default: Scons will try to find each flavour). 
    '''
    start_time =  current_time()
    source_file  = str(source[0])
    target_file  = str(target[0])
    target_dir   = os.path.dirname(target_file)
    check_source_code_extension(source_file, 'stata')
    log_file = target_dir + '/sconscript.log'
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
                command   = stata_command_win("%%STATAEXE%%")
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
    end_time = current_time()
    log_timestamp(start_time, end_time, log_file)
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

def is_in_path(program):
    # General helper function to check if `program` exist in the path env
    if is_exe(program):
        return program
    else:
        for path in os.environ['PATH'].split(os.pathsep):
            path = path.strip("'")
            exe = os.path.join(path, program)
            if is_exe(exe):
                return exe
    return None

def is_exe(file_path):
    return os.path.isfile(file_path) and os.access(file_path, os.X_OK)

def log_timestamp(start_time, end_time, filename):
    with open(filename, mode = 'r+U') as f:
        content = f.read()
        f.seek(0, 0)
        f.write('Log created:    ' + start_time + '\n' + 
                'Log completed:  ' + end_time   + '\n \n' + content)
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

def current_time():
    return datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')    
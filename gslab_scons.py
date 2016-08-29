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
from sys import platform
from gslab_fill.tablefill import tablefill

def start_log(log = "sconstruct.log"):
    if is_unix():
        sys.stdout = os.popen("tee %s" % log, "w")
    elif platform == "win32":
        sys.stdout = open(log, "w")

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
    newpdf      = source_file.replace('.lyx','.pdf')
    log_file    = target_dir + '/sconscript.log'
    os.system('lyx -e pdf2 %s > %s' % (source_file, log_file))
    shutil.move(newpdf, target_file)
    return None

def build_r(target, source, env):
    source_file = str(source[0])
    target_file = str(target[0])
    target_dir  = os.path.dirname(target_file)
    log_file    = target_dir + '/sconscript.log'
    os.system('R CMD BATCH --no-save %s %s' % (source_file, log_file))
    return None

def build_stata(target, source, env):
    source_file  = str(source[0])
    target_file  = str(target[0])
    target_dir   = os.path.dirname(target_file)

    # List of flavors to be tried, dependent on input
    user_flavor  = env["user_flavor"]  
    flavors      = ["StataMP", "StataSE", "Stata"]
    if user_flavor != None:
        flavors  = [user_flavor]

    log_file = target_dir + '/sconscript.log'
    loc_log  = os.path.basename(source_file).replace('.do','.log')
    
    for flavor in flavors:
        try: 
            if is_unix():
                command = stata_command_unix(flavor)
            elif platform == "win32":
                command = stata_command_win(flavor)
            subprocess.check_output(command % source_file, shell = True)
            break
        except subprocess.CalledProcessError:
            continue

    shutil.move(loc_log, log_file)
    return None

def stata_command_unix(flavor):
    options = {"darwin": "-e",
               "linux" : "-b",
               "linux2": "-b"}
    option  = options[platform]
    flavor  = str.lower(flavor)
    if flavor != "stata":
        flavor = flavor.replace("stata", "stata-")
    command  =  flavor + " " + option + " %s "
    return command

def stata_command_win(flavor):
    if is_64_windows():
        flavor = flavor + "-64"
    command  = flavor + ".exe " + "/e" + " %s "
    return command

def is_unix():
    unix = ["darwin", "linux", "linux2"]
    return platform in unix

def is_64_windows():
    return 'PROGRAMFILES(X86)' in os.environ
    
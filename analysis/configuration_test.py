#!/usr/bin/python
import sys
import os
import re
import subprocess
import warnings
from shutil import copyfile
from gslab_scons import _exception_classes
from gslab_scons import misc

def configuration_test(ARGUMENTS, gslab_python_version):
    # Determines whether to print traceback messages
    debug = ARGUMENTS.get('debug', False) 
    if not debug:
        # Hide traceback for configuration test only
        # http://stackoverflow.com/questions/27674602/hide-traceback-unless-a-debug-flag-is-set
        sys.tracebacklimit = 0 

    # Checks initial prerequisites
    try:
        from gslab_scons import configuration_tests as config
    except ImportError:
        message = 'Your gslab_tools Python modules installation is outdated'
        raise Exception(message)

    config.check_python(gslab_python_version = gslab_python_version, 
                        packages = ["yaml", "gslab_scons", "gslab_fill"])

    
    lfs_require    = misc.load_yaml_value("config_global.yaml", "git-lfs")
    r_require      = misc.load_yaml_value("config_global.yaml", "R")
    stata_require  = misc.load_yaml_value("config_global.yaml", "Stata")
    lyx_require    = misc.load_yaml_value("config_global.yaml", "Lyx")    

    if lfs_require:
        config.check_lfs()
    if r_require:
        config.check_r()
    if stata_require:
        config.check_stata()
    if lyx_require:
        config.check_lyx()
        
    if not os.path.isfile("config_user.yaml"):
        copyfile("config_user_template.yaml", "config_user.yaml")

    # Loads arguments and configurations
    mode = ARGUMENTS.get('mode', 'develop') # Gets mode; defaults to 'develop'

    # Checks mode/version
    if not (mode in ['develop', 'cache']):
        message = "Error: %s is not a defined mode" % mode
        raise _exception_classes.PrerequisiteError(message)

    stata_executable = misc.load_yaml_value("config_user.yaml", "stata_executable")
    # Get return list
    if mode == 'cache':
        cache_dir   = misc.load_yaml_value("config_user.yaml", "cache_directory")
        cache_dir   = misc.check_and_expand_path(cache_dir)
        return_list = [mode, stata_executable, cache_dir]
    else:
        return_list = [mode, stata_executable, None]

    # Restore default tracebacklimit and return values
    sys.tracebacklimit = 1000

    return return_list

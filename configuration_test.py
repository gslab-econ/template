#!/usr/bin/python
import sys
import os
import re
import subprocess
import warnings
from gslab_scons import _exception_classes

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
    config.check_lyx()
    config.check_lfs()
    stata_executable = config.check_stata(["yaml"])

    # Uncomment if using
    # config.check_r(packages = ["yaml"]) 

    # Loads arguments and configurations
    mode = ARGUMENTS.get('mode', 'develop') # Gets mode; defaults to 'develop'

    # Checks mode/version
    if not (mode in ['develop', 'cache']):
        message = "Error: %s is not a defined mode" % mode
        raise _exception_classes.PrerequisiteError(message)
    
    # Get return list
    if mode == 'cache':
        cache_dir   = config.load_yaml_value("user-config.yaml", "cache")
        cache_dir   = config.check_and_expand_cache_path(cache_dir)
        return_list = [mode, stata_executable, cache_dir]
    else:
        return_list = [mode, stata_executable, None]

    # Restore default tracebacklimit and return values
    sys.tracebacklimit = 0

    return return_list

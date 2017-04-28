#!/usr/bin/python
import sys
import os
import re
import subprocess
import warnings
from gslab_scons import configuration_tests
from gslab_scons import _exception_classes

def configuration_test(ARGUMENTS):
    # Determines whether to print traceback messages
    debug = ARGUMENTS.get('debug', False) 
    if not debug:
        # Hide traceback for configuration test only
        # http://stackoverflow.com/questions/27674602/hide-traceback-unless-a-debug-flag-is-set
        sys.tracebacklimit = 0 

    # Checks initial prerequisites
    configuration_tests.check_python(gslab_python_version = '3.0.5', 
                                     packages = ["yaml", "gslab_scons", "gslab_fill"])
    configuration_tests.check_lyx()
    configuration_tests.check_lfs()

    # Uncomment if using
    # configuration_tests.check_r(packages = ["yaml", "Hmisc"]) 

    # Loads arguments and configurations
    mode = ARGUMENTS.get('mode', 'develop') # Gets mode; defaults to 'develop'

    # Check stata
    sf = configuration_tests.check_stata(["yaml"])

    # Checks mode/version
    if not (mode in ['develop', 'cache']):
        raise _exception_classes.PrerequisiteError("Error: %s is not a defined mode" % mode)
    
    # Get return list
    if mode == 'cache':
        cache_dir   = configuration_tests.load_yaml_value("user-config.yaml", "cache")
        cache_dir   = configuration_tests.check_and_expand_cache_path(cache_dir)
        return_list = [mode, sf, cache_dir]
    else:
        return_list = [mode, sf, None]

    # Restore default tracebacklimit and return values
    sys.tracebacklimit = 0

    return return_list



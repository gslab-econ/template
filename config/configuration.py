#!/usr/bin/python
import os
import sys
import warnings
import yaml
from gslab_scons import _exception_classes, misc
from gslab_scons import configuration_tests as config

def configuration(ARGUMENTS, paper = False, config_user_yaml = 'config_user.yaml',
                  config_global_yaml = 'config_global.yaml'):
    # Determines whether to print traceback messages
    debug = ARGUMENTS.get('debug', False)
    if not debug:
        # Hide traceback for configuration test only
        # http://stackoverflow.com/questions/27674602/hide-traceback-unless-a-debug-flag-is-set
        sys.tracebacklimit = 100

    # Checks git-lfs
    prereq_gitlfs = misc.load_yaml_value(config_global_yaml, 'prereq_git-lfs')
    if prereq_gitlfs:
        config.check_lfs()

    # Check lyx or latex
    if paper:
        prereq_lyx   = misc.load_yaml_value(config_global_yaml, 'prereq_Lyx')
        prereq_latex = misc.load_yaml_value(config_global_yaml, 'prereq_Latex')
        if prereq_lyx:
            config.check_lyx()
        if prereq_latex:
            pass

    # Loads arguments and configurations
    mode = ARGUMENTS.get('mode', 'develop') # Gets mode; defaults to 'develop'
    vers = ARGUMENTS.get('version', '')

    # Checks mode/version
    if not (mode in ['develop', 'cache']):
        message = 'Error: %s is not a defined mode' % mode
        raise _exception_classes.PrerequisiteError(message)

    # Checks for cache directory
    if mode == 'cache':
        cache_dir = misc.load_yaml_value(config_user_yaml, 'cache_directory')
        cache_dir = misc.check_and_expand_path(cache_dir)
    else:
        cache_dir = None

    # Loads config yaml files
    PATHS = {'user': config_user_yaml, 'global': config_global_yaml}
    for key, val in PATHS.items():
        if os.path.isfile(val):
            PATHS[key] = yaml.load(open(val, 'rU'))
        else:
            del PATHS[key]

    # Stores PYTHONPATH
    try:
        pythonpath = os.environ['PYTHONPATH']
    except KeyError:
        pythonpath = ''
    
    # Get return list
    return_list = [mode, vers, cache_dir, PATHS, pythonpath]

    # Restore default tracebacklimit and return values
    sys.tracebacklimit = 1000

    return return_list

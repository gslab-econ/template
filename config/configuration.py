#!/usr/bin/python
import sys
import warnings
from gslab_scons import _exception_classes
from gslab_scons import misc
from gslab_scons import configuration_tests as config

def configuration(ARGUMENTS, paper = False, config_user_yaml = 'config_user.yaml',
                  config_global_yaml = 'config_global.yaml'):
    # Determines whether to print traceback messages
    debug = ARGUMENTS.get('debug', False)
    if not debug:
        # Hide traceback for configuration test only
        # http://stackoverflow.com/questions/27674602/hide-traceback-unless-a-debug-flag-is-set
        sys.tracebacklimit = 0

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

    # Get return list
    if mode == 'cache':
        cache_dir   = misc.load_yaml_value(config_user_yaml, 'cache_directory')
        cache_dir   = misc.check_and_expand_path(cache_dir)
        return_list = [mode, vers, cache_dir]
    else:
        return_list = [mode, vers, None]

    # Restore default tracebacklimit and return values
    sys.tracebacklimit = 1000

    return return_list

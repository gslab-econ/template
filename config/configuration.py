#!/usr/bin/python
import os
import sys
import shutil
import warnings
import yaml

from gslab_scons import _exception_classes, misc
from gslab_scons import check_prereq

def configuration(ARGUMENTS, paper = False, config_user_yaml = 'config_user.yaml',
                  config_global_yaml = 'config_global.yaml'):
    # Determines whether to print traceback messages
    debug = ARGUMENTS.get('debug', False)
    if not debug:
        # Hide traceback for configuration test only
        # http://stackoverflow.com/questions/27674602/hide-traceback-unless-a-debug-flag-is-set
        sys.tracebacklimit = 100

    # Copies config_user template if no such file exists
    if not os.path.isfile(config_user_yaml):
        shutil.copy('../config/config_user_template.yaml', config_user_yaml)

    # Loads arguments and configurations
    mode = ARGUMENTS.get('mode', 'develop') # Gets mode; defaults to 'develop'

    # Checks mode
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
    CONFIG = {'user': config_user_yaml, 'global': config_global_yaml}
    for key, val in CONFIG.items():
        CONFIG[key] = yaml.load(open(val, 'rU'))
        if not CONFIG[key]:
            del CONFIG[key]

    # Stores executable names and prerequisite checks. Prefer user to global.
    executable_names = misc.add_two_dict_keys(d = CONFIG, common_key = 'executable_names')
    prereq_checks = misc.add_two_dict_keys(d = CONFIG, common_key = 'prereq_checks')

    # Checks prerequisite applications and record known prereqs
    prereqs = []
    for prereq, should_check_prereq in prereq_checks.items():
        if str(should_check_prereq).lower().strip() in ['y', 'yes', 't', 'true']:
            check_prereq(prereq, manual_execs = executable_names, 
                         gslab_vers = CONFIG['global']['gslab_version'])
            prereqs.append(prereq)

    # Stores PYTHONPATH
    try:
        pythonpath = os.environ['PYTHONPATH']
    except KeyError:
        pythonpath = ''
    
    # Gets return list
    return_list = [mode, cache_dir, CONFIG, executable_names, prereqs, pythonpath]

    # Restores default tracebacklimit and return values
    sys.tracebacklimit = 1000

    return return_list

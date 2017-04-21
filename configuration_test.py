#!/usr/bin/python
import sys
import os
import re
import subprocess
import pkg_resources
import warnings

def configuration_test(ARGUMENTS):
    # Determines whether to print traceback messages
    debug = ARGUMENTS.get('debug', False) 
    if not debug:
        # Hide traceback for configuration test only
        # http://stackoverflow.com/questions/27674602/hide-traceback-unless-a-debug-flag-is-set
        sys.tracebacklimit = 0 

    # Checks initial prerequisites
    check_python()
    check_lyx()
    check_gitlfs()
    check_yamls()

    # Uncomment if using
    #check_r() 
    #check_gslab_metropolis() 

    # Loads arguments and configurations
    mode = ARGUMENTS.get('mode', 'develop') # Gets mode; defaults to 'develop'

    # Check stata
    sf = check_stata(ARGUMENTS)

    # Checks mode/version
    if not (mode in ['develop', 'cache']):
        raise PrerequisiteError("Error: %s is not a defined mode" % mode)
    
    # Get return list
    if mode == 'cache':
        cache_dir   = load_yaml_value("user-config.yaml", "cache")
        cache_dir   = check_and_expand_cache_path(cache_dir)
        return_list = [mode, sf, cache_dir]
    else:
        return_list = [mode, sf, None]

    # Restore default tracebacklimit and return values
    sys.tracebacklimit = 0
    return return_list

def check_python():
    if sys.version_info[0] != 2:
        raise PrerequisiteError('Please use python 2')
    check_python_packages()

def check_python_packages():
    try:
        import gslab_scons
        import gslab_make
        import gslab_fill
    except:
        raise PrerequisiteError('Missing gslab_python modules')

    try:
        import yaml
    except:
        raise PrerequisiteError('Missing PyYAML python module')

    if pkg_resources.get_distribution('gslab_tools').version < '3.0.3':
        raise PrerequisiteError('Wrong version of gslab_python modules')

def check_r():
    from gslab_scons.misc import is_in_path
    if is_in_path('R.exe') is None and is_in_path('R') is None:
        raise PrerequisiteError('R is not installed or excecutable is not added to path')
    check_r_packages()

def check_r_packages():
    for pkg in ["yaml"]:
        # http://stackoverflow.com/questions/6701230/call-r-function-in-linux-command-line
        # and http://stackoverflow.com/questions/18962785/oserror-errno-2-no-such-file-or-directory-while-using-python-subprocess-in-dj
        subprocess.check_output('R -q -e "library(%s)"' % pkg, shell = True)

def check_lyx():
    from gslab_scons.misc import is_in_path
    if is_in_path('lyx.exe') is None and is_in_path('lyx') is None:
        raise PrerequisiteError('Lyx is not installed or excecutable is not added to path')

def check_gslab_metropolis():
    if sys.platform == 'win32':
        warnings.warn('It has not been tested whether gslab metropolis beamer is installed or not.' + \
            'Please make sure it has been installed before running the repo.')
    else:
        metropolis_path = '/usr/local/texlive/texmf-local/tex/latex/' + \
                          'beamer/themes/gslab/beamerthememetropolis_gslab.sty'
        if os.path.isfile(metropolis_path):
            pass
        else:
            raise PrerequisiteError('gslab metropolis beamer not found at %s' % metropolis_path)

def check_gitlfs():
    from gslab_scons.misc import check_lfs
    try:
        check_lfs()
    except:
        raise PrerequisiteError("Please ensure git-lfs is installed.")

def check_yamls():
    for f in ["constants.yaml"]:
        if not os.path.isfile(f):
            raise PrerequisiteError("%s file does not exist. Please create it." % f)

def check_and_expand_cache_path(cache):
    error_message = " Cache directory, '%s', is not created. " % cache + \
                    "Please manually create before running.\n\t\t" + \
                    "    Or fix the path in user-config.yaml.\n"
    try:
        cache = os.path.expanduser(cache)
        if not os.path.isdir(cache):
            raise PrerequisiteError(error_message)
        return cache
    except:
        raise PrerequisiteError(error_message)


def check_stata(ARGUMENTS):
    import yaml
    import gslab_scons.misc as misc

    sf_configs = load_yaml_value("user-config.yaml", "stata_executable")
    sf         = ARGUMENTS.get('sf', sf_configs) 

    # Fake scons-like env dict for misc.get_stata_executable(env)
    fake_env = {'user_flavor': sf} 
    stata_exec = misc.get_stata_executable(fake_env)
    
    if stata_exec is None:
        raise PrerequisiteError('Stata is not installed or executable is not added to path')
    
    command = misc.get_stata_command(stata_exec)
    check_stata_packages(command)
    return sf

def load_yaml_value(path, key):
    import yaml

    if key == "stata_executable":
        prompt = "Enter %s value or None to search for defaults: "
    else:
        prompt = "Enter %s value: "

    # Check if file exists and is not corrupted. 
    # If so, load yaml contents.
    yaml_contents = None
    if os.path.isfile(path):
        try:
            yaml_contents = yaml.load(open(path, 'rU'))
        except yaml.scanner.ScannerError:
            message  = "%s is a corrupted yaml file. Delete file and recreate? (y/n) "
            response = str(raw_input(message % path))
            if response.lower() == 'y':
                os.remove(path)
                yaml_contents = None
            else:
                raise PrerequisiteError("%s is a corrupted yaml file. Please fix." % path)

    # If key exists, return value.
    # Otherwise, add key-value to file.
    try:
        if yaml_contents[key] == "None":
            return None
        else:
            return yaml_contents[key]
    except:
        with open(path, 'ab') as f:        
            val = str(raw_input(prompt % key))
            if re.sub('"', '', re.sub('\'', '', val.lower())) == "none":
                val = None
            f.write('\n%s: %s\n' % (key, val))
        return val

def check_stata_packages(command):
    import gslab_scons.misc as misc
    if misc.is_unix():
        command = command.split("%s")[0]
    elif sys.platform == "win32":
        command = command.split("do")[0]

    try:
        for pkg in ['yaml']:
            call = (command + "which %s") % pkg
            # http://www.stata.com/statalist/archive/2009-12/msg00493.html 
            # and http://stackoverflow.com/questions/18962785/oserror-errno-2-no-such-file-or-directory-while-using-python-subprocess-in-dj
            subprocess.check_output(call, stderr = subprocess.STDOUT, shell = True) 
            with open('stata.log', 'rU') as f:
                log = f.read()
    except subprocess.CalledProcessError:
        raise PrerequisiteError("Stata command, '%s', failed.\n" % command.split(' ')[0] + \
                                "\t\t   Please supply a correct stata_executable" + \
                                " value in user_config.yaml.\n" )

    os.remove('stata.log')
    if re.search('command %s not found' % pkg, log):
        raise PrerequisiteError('Stata package %s is not installed' % pkg)

class PrerequisiteError(Exception):
    pass

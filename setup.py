import sys
import os
import re
import subprocess
import pkg_resources
import warnings

def setup_test(ARGUMENTS):
    check_python()
    check_r()
    check_lyx()
    check_metropolis()
    check_gitlfs()
    check_yamls()

    # Loads arguments and configurations
    import yaml
    user_configs = yaml.load(open("user-config.yaml", 'rU'))
    mode         = ARGUMENTS.get('mode', 'develop') # Gets mode; defaults to 'develop'
    # Gets user supplied stata from command line or yaml
    sf_configs   = user_configs.get('stata_flavor', None) 
    sf           = ARGUMENTS.get('sf', sf_configs) 
    cache_dir    = user_configs['cache']
    if mode in ['cache', 'release']:
        check_cache(cache)

    # Check stata after loading sf
    check_stata(sf)

    # Checks mode/version
    if not (mode in ['develop', 'cache']):
        raise PrerequisiteError("Error: %s is not a defined mode" % mode)

    # Returns arguments and configurations
    return [user_configs, mode, sf, cache_dir]

def check_python():
    if sys.version_info[0] != 2:
        raise PrerequisiteError('Not the right version of python')
    check_python_packages()

def check_python_packages():
    try:
        import gslab_scons
        import gslab_make
        import gslab_fill
    except:
        raise PrerequisiteError('Missing gslab_tools python module')

    try:
        import yaml
    except:
        raise PrerequisiteError('Missing PyYAML python module')

    if pkg_resources.get_distribution('gslab_tools').version < '3.0.3':
        raise PrerequisiteError('Wrong version of gslab_tools')

def check_r():
    from gslab_scons.misc import is_in_path
    if is_in_path('R.exe') is None and is_in_path('R') is None:
        raise PrerequisiteError('R is not installed or excecutable is not added to path')
    check_r_packages()

def check_r_packages():
    for pkg in ["yaml"]:
        subprocess.check_output('R -q -e "library(%s)"' % pkg, shell = True) # http://stackoverflow.com/questions/6701230/call-r-function-in-linux-command-line and http://stackoverflow.com/questions/18962785/oserror-errno-2-no-such-file-or-directory-while-using-python-subprocess-in-dj

def check_lyx():
    from gslab_scons.misc import is_in_path
    if is_in_path('lyx.exe') is None and is_in_path('lyx') is None:
        raise PrerequisiteError('Lyx is not installed or excecutable is not added to path')

def check_metropolis():
    if sys.platform == 'win32':
        warnings.warn('It has not been tested whether Metropolis beamer is installed or not.' + \
            'Please make sure it has been installed before running the repo.')
    else:
        metropolis_path = '/usr/local/texlive/texmf-local/tex/latex/' + \
                          'beamer/themes/gslab/beamerthememetropolis_gslab.sty'
        if os.path.isfile(metropolis_path):
            pass
        else:
            raise PrerequisiteError('Metropolis beamer not found at %s' % metropolis_path)

def check_gitlfs():
    from gslab_scons.misc import check_lfs
    check_lfs()

def check_yamls():
    for f in ["constants.yaml", "user-config.yaml"]:
        if not os.path.isfile(f):
            raise PrerequisiteError("%s file does not exist. Please create it." % f)

def check_cache(cache):
    if not os.path.isdir(cache):
        raise PrerequisiteError("Cache directory (%s) is not created." + \
                                "Please manually create before running." % cache)

def check_stata(sf):
    import gslab_scons.misc as misc

    # Fake scons-like env dict for misc.get_stata_executable(env)
    fake_env = {'user_flavor': sf} 
    stata_exec = misc.get_stata_executable(fake_env)
    
    if stata_exec is None:
        raise PrerequisiteError('Stata is not installed or executable is not added to path')
    
    command = misc.get_stata_command(stata_exec)
    check_stata_packages(command)

def check_stata_packages(command):
    import gslab_scons.misc as misc
    if misc.is_unix():
        command = command.split("%s")[0]
    elif sys.platform == "win32":
        command = command.split("do")[0]

    for pkg in ['yaml']:
        subprocess.check_output(command + "which %s" % pkg , shell = True) # http://www.stata.com/statalist/archive/2009-12/msg00493.html and http://stackoverflow.com/questions/18962785/oserror-errno-2-no-such-file-or-directory-while-using-python-subprocess-in-dj
        with open('stata.log', 'rU') as f:
            log = f.read()
        if re.search('command %s not found' % pkg, log):
            raise PrerequisiteError('Stata package %s is not installed' % pkg)
        os.remove('stata.log')

class PrerequisiteError(Exception):
    pass



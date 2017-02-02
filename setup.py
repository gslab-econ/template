import sys
import os
import subprocess
import pkg_resources
from sys import platform
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
    sf           = ARGUMENTS.get('sf', user_configs['stata_flavor']) # Gets user supplied stata from command line or yaml
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

def check_stata(sf):
    import gslab_scons.misc as misc
    command = ''
    flavors = ['stata-mp', 'stata-se', 'stata']
    if sf is not None:
        flavors = [sf] + flavors
    if misc.is_unix():
        for flavor in flavors:
            if misc.is_in_path(flavor):
                command = misc.stata_command_unix(flavor)
                break
    elif platform == 'win32':
        try:
            key_exist = os.environ['STATAEXE'] is not None
            command   = misc.stata_command_win("%%STATAEXE%%")
        except KeyError:
            flavors = [(f.replace('-', '') + '.exe') for f in flavors]
            if misc.is_64_windows():
                flavors = [f.replace('.exe', '-64.exe') for f in flavors]
            for flavor in flavors:
                if misc.is_in_path(flavor):
                    command = misc.stata_command_win(flavor)
                    break        
    if command == '':
        raise PrerequisiteError('Stata is not installed or excecutable is not added to path')

    check_stata_packages(command)

def check_stata_packages(command):
    pass
    #for pkg in ['yaml', 'AKG']:
    #    os.system(command % '"which %s"' % pkg) # http://www.stata.com/statalist/archive/2009-12/msg00493.html

def check_r():
    from gslab_scons.misc import is_in_path
    if is_in_path('R.exe') is None and is_in_path('R') is None:
        raise PrerequisiteError('R is not installed or excecutable is not added to path')
    check_r_packages()

def check_r_packages():
    pass
    #for pkg in ["yaml", 'SOEMME']:
        #try:
    #    os.system('R -q -e "library(%s)"' % pkg) # http://stackoverflow.com/questions/6701230/call-r-function-in-linux-command-line
        #except:
         #   raise PrerequisiteError("R package %s is not installed." % pkg)

def check_lyx():
    from gslab_scons.misc import is_in_path
    if is_in_path('lyx.exe') is None and is_in_path('lyx') is None:
        raise PrerequisiteError('Lyx is not installed or excecutable is not added to path')

def check_metropolis():
    if platform == 'win32':
        warnings.warn('It has not been tested whether Metropolis beamer is installed or not. Please make sure it has been installed before running the repo.')
    else:
        if os.path.isfile('/usr/local/texlive/texmf-local/tex/latex/beamer/themes/gslab/beamerthememetropolis_gslab.sty'):
            pass
        else:
            raise PrerequisiteError('Metropolis beamer not found at /usr/local/texlive/texmf-local/tex/latex/beamer/themes/gslab')

def check_gitlfs():
    from gslab_scons.misc import check_lfs
    check_lfs()

def check_cache(cache):
    if not os.path.isdir(cache):
        raise PrerequisiteError("Cache directory (%s) is not created. Please manually create before running." % cache)

def check_yamls():
    if not os.path.isfile("constants.yaml"):
        raise PrerequisiteError("constants.yaml file does not exist. Please create it.")
    if not os.path.isfile("user-config.yaml"):
        raise PrerequisiteError("user-config.yaml file does not exist. Please create it.")

class PrerequisiteError(Exception):
    pass



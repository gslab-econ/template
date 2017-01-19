import sys
import os
import subprocess
import pkg_resources

def setup_test(mode, vers, sf):
    check_os()
    check_python()
    check_gslab_tools()
    check_stata(sf)
    check_r()
    check_lyx()
    check_metropolis()
    check_gitlfs()

    # Sets up logs and checks mode/version
    if not (mode in ['develop', 'cache', 'release']):
        print("Error: %s is not a defined mode" % mode)
        sys.exit()

    if mode == 'release' and vers == '':
        print("Error: Version must be defined in release mode")
        sys.exit()

def check_os():
    if sys.platform not in ['darwin', 'linux', 'linux2']:
        raise PrerequisiteError('Not the right operating system')

def check_python():
    if sys.version_info[0] != 2:
        raise PrerequisiteError('Not the right version of python')

def check_gslab_tools():
    try:
        import gslab_scons
        import gslab_make
        import gslab_fill
    except:
        raise PrerequisiteError('Missing gslab_tools')

    if pkg_resources.get_distribution('gslab_tools').version < '1.1.1':
        raise PrerequisiteError('Wrong version of gslab_tools')

def check_stata(sf):
    import gslab_scons.misc as misc
    if sf is not None:
        if misc.is_in_path(sf) is None:
            raise PrerequisiteError('User supplied stata command, %s, is not installed in path.' % sf)
    else:
        command = ''
        flavors = ['stata-mp', 'stata-se', 'stata']
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

def check_r():
    from gslab_scons.misc import is_in_path
    if is_in_path('R') is None:
        raise PrerequisiteError('R is not installed or excecutable is not added to path')

def check_lyx():
    from gslab_scons.misc import is_in_path
    if is_in_path('lyx') is None:
        raise PrerequisiteError('Lyx is not installed, or excecutable is not added to path, or GSLab-modified Metropolis beamer theme is not added')

def check_metropolis():
    if os.path.isfile('/usr/local/texlive/texmf-local/tex/latex/beamer/themes/gslab/beamerthememetropolis_gslab.sty'):
        pass
    else:
        raise PrerequisiteError('Metropolis beamer not found at /usr/local/texlive/texmf-local/tex/latex/beamer/themes/gslab')

def check_gitlfs():
    from gslab_scons.misc import check_lfs
    check_lfs()

class PrerequisiteError(Exception):
    pass



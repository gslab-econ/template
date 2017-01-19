import sys
import os
import subprocess
import pkg_resources

def main():
    check_os()
    check_python()
    check_stata()
    check_r()
    check_lyx()
    check_scons()
    check_gslab_tools()
    check_gitlfs()

    print "\n\nCongratulations! You have satisfied all pre-requisites!"

class PrerequisiteError(Exception):
    pass

def check_os():
    if sys.platform not in ['darwin', 'linux', 'linux2']:
        raise PrerequisiteError('Not the right operating system')

def check_python():
    if sys.version_info[0] != 2:
        raise PrerequisiteError('Not the right version of python')

def check_stata():
    os.system('echo "gen x = 1" > test.do')
    try:
        subprocess.call(['statamp', '-e', 'test.do'])
    except OSError:
        raise PrerequisiteError('Stata is not installed or excecutable is not added to path')
    os.system('rm test.do test.log')

def check_r():
    os.system('echo "x <- 1" > test.R')
    try:
        subprocess.call(['Rscript', 'test.R'])
    except OSError:
        raise PrerequisiteError('R is not installed or excecutable is not added to path')
    os.system('rm test.R')

def check_lyx():
    try:
       subprocess.call(['lyx', '--export', 'pdf', 'source/paper/paper.lyx'])
    except OSError:
        print('Lyx is not installed, or excecutable is not added to path')
    os.system('rm source/paper/paper.pdf')

def check_scons():
    try:
        subprocess.call(['scons', '--version'])
    except:
        raise PrerequisiteError('SCons is not installed')

def check_gslab_tools():
    try:
        import gslab_scons
        import gslab_make
        import gslab_fill
    except:
        raise PrerequisiteError('Missing gslab_tools')

    if pkg_resources.get_distribution('gslab_tools').version < '1.1.1':
        raise PrerequisiteError('Wrong version of gslab_tools')

def check_gitlfs():
    try:
        subprocess.call(['git', 'lfs', 'version'])
    except:
        raise PrerequisiteError('Git-lfs is not installed')

main()

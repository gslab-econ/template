import sys
import os
import subprocess

# Check operating system
if sys.platform not in ['darwin', 'linux', 'linux2']:
    raise SystemError('Not the right operating system')

# Check python version
if sys.version_info[0] != 2:
    raise VersionError('Not the right version of python')

# Check if Stata is installed and executable added to path
os.system('echo "gen x = 1" > test.do')
try:
    subprocess.call(['statamp', '-e', 'test.do'])
except OSError:
    print('Stata is not installed or excecutable is not added to path')
os.system('rm test.do test.log')

# Check if R is installed and executable added to path
os.system('echo "x <- 1" > test.R')
try:
    subprocess.call(['Rscript', 'test.R'])
except OSError:
    print('R is not installed or excecutable is not added to path')
os.system('rm test.R')

# Check if lyx is installed and executable added to path
try:
    subprocess.call(['lyx', '--export', 'pdf', 'source/paper/paper.lyx'])
except OSError:
    print('Lyx is not installed or excecutable is not added to path')
os.system('rm source/paper/paper.pdf')

# Check gslab_tools
try:
    import gslab_scons
    import gslab_make
    import gslab_fill
except ImportError:
    print('Missing gslab_tools')

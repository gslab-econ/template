import pip
import sys
import subprocess


def main(filename='config/requirements.txt', upgrade=False):
    
    # Install base python requirements, if they are not installed or are the wrong version
    command = [sys.executable, '-m', 'pip', 'install', '-r', filename]
    if upgrade:
        command.append('--upgrade')
    subprocess.check_call(command)
    return None

    # Install gslab_tools
    subprocess.call(['pip', 'install', "git+https://git@github.com/gslab-econ/gslab_python.git@master"])

# upgrade = TRUE will update all packages to the most current version
# The default option will skip packages that are already installed
main()



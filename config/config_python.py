import pip
import sys
import subprocess


def main(filename='config/requirements.txt', upgrade=False):
    # Install gslab_tools if it's not installed yet or it has the wrong version
    command = [sys.executable, '-m', 'pip', 'install', '-r', filename]
    if upgrade:
        command.append('--upgrade')
    subprocess.check_call(command)
    return None


# upgrade = TRUE will update all packages to the most current version
# The default option will skip packages that are already installed
main()

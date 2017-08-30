import pip
import pkg_resources

def main():
    # Install gslab_tools if it's not installed yet or it has the wrong version
    if not check_gslab_tools('4.1.0'):
        pip.main(['install', 'git+http://git@github.com/gslab-econ/gslab_python.git@4.1.0'])

    # Install required packages using pip
    packages = {'pyyaml': True}
    installed_packages = [pkg.key for pkg in pip.get_installed_distributions()]
    for pkg in packages.keys():
        if pkg not in installed_packages or packages[pkg]:
            pip.main(['install', '--upgrade', pkg])

def check_gslab_tools(gslab_python_version):
    try:
        installed = pkg_resources.get_distribution('gslab_tools').version.split('.')
    except pkg_resources.DistributionNotFound:
        return False

    installed = int(installed[0]) * 10000 + \
                int(installed[1]) * 100 + \
                int(installed[2])
    required = str(gslab_python_version).split('.')
    required = int(required[0]) * 10000 + \
               int(required[1]) * 100 + \
               int(required[2])
    if installed < required:
        return False
    else:
        return True

main()

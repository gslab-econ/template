import pip
import pkg_resources
# *** Add required packages to this list ***
packages = ['pyyaml', 'numpy', 'matplotlib']
# *** Add required packages to this list ***

def main(packages, upgrade = False):
    # Install gslab_tools if it's not installed yet or it has the wrong version
    pip.main(['install', '--upgrade', 'git+http://git@github.com/gslab-econ/gslab_python.git@v4.1.0'])

    # Install required packages using pip
    installed_packages = [pkg.key for pkg in pip.get_installed_distributions()]
    for pkg in packages:
        if upgrade:
            pip.main(['install', '--upgrade', pkg])
        elif pkg not in installed_packages:
            pip.main(['install', pkg])

# upgrade = TRUE will update all packages to the most current version
# upgrade = FALSE will skip packages that are already installed
main(packages, upgrade = False)

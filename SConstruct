# Preliminaries
import os
import sys
import re
import yaml

user_configs = yaml.load(open("user-config.yaml", 'rU'))

mode      = ARGUMENTS.get('mode', 'develop') # Gets mode; defaults to 'develop'
vers      = ARGUMENTS.get('version', '') # Gets release version; defaults to ''
sf        = ARGUMENTS.get('sf', user_configs['stata_flavor']) # Gets user supplied stata or defaults to None
cache_dir = user_configs['cache']

# Test for proper prerequisites and setup; import gslab_scons after passing setup
from setup import setup_test
setup_test(mode, vers, sf, cache_dir)
import gslab_scons 

# Start log
gslab_scons.start_log() 


# Defines environment
env = Environment(ENV = {'PATH' : os.environ['PATH']}, 
                  IMPLICIT_COMMAND_DEPENDENCIES = 0,
                  BUILDERS = {'Tablefill'   : Builder(action = gslab_scons.build_tables),
                              'BuildLyx'    : Builder(action = gslab_scons.build_lyx),
                              'BuildR'      : Builder(action = gslab_scons.build_r),
                              'BuildStata'  : Builder(action = gslab_scons.build_stata),
                              'BuildPython' : Builder(action = gslab_scons.build_python)},
                  user_flavor = sf)

env.Decider('MD5-timestamp') # Only computes hash if time-stamp changed
env.EXTENSIONS = ['.eps', '.pdf', '.lyx'] # Extensions to be used when scanning for source files in BuildLyx.
SourceFileScanner.add_scanner('.lyx', Scanner(gslab_scons.misc.lyx_scan, recursive = True))

# Load paths
env['PATHS'] = yaml.load(open("constants.yaml", 'rU'))

# Export environment
Export('env')

# Run sub-trees
SConscript('source/data/SConscript') 
SConscript('source/analysis/SConscript')
SConscript('source/tables/SConscript') 
SConscript('source/paper/SConscript') 
SConscript('source/talk/SConscript') 
Default('./build', './release')

# Additional mode options
if mode == 'cache':
    CacheDir(cache_dir)

# Print the state of the repo at end of SCons run
finish_command = Command( 'state_of_repo.log', [], gslab_scons.misc.state_of_repo, MAXIT=10) # From http://stackoverflow.com/questions/8901296/how-do-i-run-some-code-after-every-build-in-scons
Depends(finish_command, BUILD_TARGETS)
env.AlwaysBuild(finish_command)
if 'state_of_repo.log' not in BUILD_TARGETS: 
    BUILD_TARGETS.append('state_of_repo.log')

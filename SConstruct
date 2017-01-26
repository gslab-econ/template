# Preliminaries
import os
import sys
import re
mode    = ARGUMENTS.get('mode', 'develop') # Gets mode; defaults to 'develop'
vers    = ARGUMENTS.get('version', '') # Gets release version; defaults to ''
sf      = ARGUMENTS.get('sf', None) # Gets user supplied stata or defaults to None
cache_dir   = '/Users/%s/Google Drive/cache/large_template'    % os.environ['USER']

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

Export('env')

# Run sub-trees
SConscript('source/data/SConscript') 
SConscript('source/analysis/SConscript')
SConscript('source/tables/SConscript') 
SConscript('source/paper/SConscript') 
SConscript('source/talk/SConscript') 

# Additional mode options
if mode == 'cache':
    CacheDir(cache_dir)

# Preliminaries
import os
import sys
import re
mode    = ARGUMENTS.get('mode', 'develop') # Gets mode; defaults to 'develop'
vers    = ARGUMENTS.get('version', '') # Gets release version; defaults to ''
sf      = ARGUMENTS.get('sf', None) # Gets user supplied stata or defaults to None
cache   = '/Users/%s/Google Drive/cache/large_template'    % os.environ['USER']
release = '/Users/%s/Google Drive/release/large_template/' % os.environ['USER']

# Test for proper prerequisites and setup
from setup import setup_test
setup_test(mode, vers, sf, cache)

# Import gslab_scons after sucessfully passing setup
import gslab_scons as builders
import gslab_scons.log as log
import gslab_scons.release as release
from gslab_scons.misc import lyx_scan

log.start_log() 

# Defines environment
env = Environment(ENV = {'PATH' : os.environ['PATH']}, 
                  IMPLICIT_COMMAND_DEPENDENCIES = 0,
                  BUILDERS = {'Tablefill'   : Builder(action = builders.build_tables),
                              'BuildLyx'    : Builder(action = builders.build_lyx),
                              'BuildR'      : Builder(action = builders.build_r),
                              'BuildStata'  : Builder(action = builders.build_stata),
                              'BuildPython' : Builder(action = builders.build_python)},
                  user_flavor = sf)

env.Decider('MD5-timestamp') # Only computes hash if time-stamp changed
env.EXTENSIONS = ['.eps', '.pdf', '.lyx'] # Extensions to be used when scanning for source files in BuildLyx.
SourceFileScanner.add_scanner('.lyx', Scanner(lyx_scan, recursive = True))

Export('env')

# Run sub-trees
SConscript('source/data/SConscript') 
SConscript('source/analysis/SConscript')
SConscript('source/tables/SConscript') 
SConscript('source/paper/SConscript') 
SConscript('source/talk/SConscript') 

# Additional mode options
if mode in ['cache', 'release']:
    CacheDir(cache)

if mode == 'release':
    # Installs files in appropriate locations for release mode
    release = release + vers + '/'
    DriveReleaseFiles = ['#build/data/data.txt']
    release.release(env, vers, DriveReleaseFiles, release, org = 'gslab-econ', repo = 'template')
    ## Specifies default targets to build
    Default('.', release)

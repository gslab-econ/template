# Preliminaries
import os
import sys
import re
mode = ARGUMENTS.get('mode', 'develop') # Gets mode; defaults to 'develop'
vers = ARGUMENTS.get('version', '') # Gets release version; defaults to ''
sf   = ARGUMENTS.get('sf', None) # Gets user supplied stata or defaults to None

# Test for proper prerequisites and setup
from setup import setup_test
setup_test(mode, vers, sf)

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
env.EXTENSIONS = ['.eps', '.txt.', '.lyx']
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
    # Defines cache in cache mode
    USER        = os.environ['USER']
    local_cache = '/Users/%s/Google Drive/cache/large_template' % USER
    os.system('mkdir -p "%s"' % local_cache)
    CacheDir(local_cache)

if mode == 'release':
    # Installs files in appropriate locations for release mode
    local_release = '/Users/%s/Google Drive/release/large_template/' % USER
    local_release = local_release + vers + '/'
    DriveReleaseFiles = ['#build/data/data.txt']
    release.release(env, vers, DriveReleaseFiles, local_release, org = 'gslab-econ', repo = 'template')
    ## Specifies default targets to build
    Default('.', local_release)

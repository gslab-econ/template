# Preliminaries
import os
import sys
import gslab_scons.build as build
import gslab_scons.log as log
import gslab_scons.release as release
mode = ARGUMENTS.get('mode', 'develop') # Gets mode; defaults to 'develop'
vers = ARGUMENTS.get('version', '') # Gets release version; defaults to ''

# Sets up logs and checks mode/version
if not (mode in ['develop', 'cache', 'release']):
    print("Error: %s is not a defined mode" % mode)
    sys.exit()

if mode == 'release' and vers == '':
    print("Error: Version must be defined in release mode")
    sys.exit()

log.start_log() 

# Defines environment
env = Environment(ENV = {'PATH' : os.environ['PATH']}, 
                  IMPLICIT_COMMAND_DEPENDENCIES = 0,
                  BUILDERS = {'Tablefill'   : Builder(action = build.build_tables),
                              'BuildLyx'    : Builder(action = build.build_lyx),
                              'BuildR'      : Builder(action = build.build_r),
                              'BuildStata'  : Builder(action = build.build_stata),
                              'BuildPython' : Builder(action = build.build_python)},
                  user_flavor = ARGUMENTS.get('sf', 'StataMP'))

env.Decider('MD5-timestamp') # Only computes hash if time-stamp changed
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



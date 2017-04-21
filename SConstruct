# Preliminaries
import os
import sys
sys.dont_write_bytecode = True # http://stackoverflow.com/questions/154443/how-to-avoid-pyc-files

# Test for proper prerequisites and setup
from configuration_test import configuration_test
[mode, sf, cache_dir] = configuration_test(ARGUMENTS)
import gslab_scons 
import gslab_scons.log as log
import yaml
import atexit

# Start log
mode = ARGUMENTS.get('mode', 'develop') # Gets mode; defaults to 'develop'
vers = ARGUMENTS.get('version', '') # Gets release version; defaults to ''
log.start_log(mode, vers)

# Defines environment
env = Environment(ENV = {'PATH' : os.environ['PATH']}, 
                  IMPLICIT_COMMAND_DEPENDENCIES = 0,
                  BUILDERS = {'Tablefill'   : Builder(action = gslab_scons.build_tables),
                              'BuildLyx'    : Builder(action = gslab_scons.build_lyx),
                              'BuildR'      : Builder(action = gslab_scons.build_r),
                              'BuildStata'  : Builder(action = gslab_scons.build_stata),
                              'BuildPython' : Builder(action = gslab_scons.build_python)},
                  user_flavor = sf)

# Only computes hash if time-stamp changed
env.Decider('MD5-timestamp') 
# Extensions to be used when scanning for source files in BuildLyx.
env.EXTENSIONS = ['.eps', '.pdf', '.lyx']
SourceFileScanner.add_scanner('.lyx', Scanner(gslab_scons.misc.lyx_scan, recursive = True))

# Load paths
env['PATHS'] = yaml.load(open("constants.yaml", 'rU'))

# Export environment
Export('env')

# Run sub-trees
SConscript('source/analysis/SConscript')
SConscript('source/tables/SConscript') 
SConscript('source/paper/SConscript') 
SConscript('source/talk/SConscript') 
Default('./build', './release')

# Additional mode options
if mode == 'cache':
    CacheDir(cache_dir)

# Print the state of the repo and issue size warnings at end of SCons run
# From http://stackoverflow.com/questions/8901296/how-do-i-run-some-code-after-every-build-in-scons
debrief = Command('state_of_repo.log', [], gslab_scons.misc.scons_debrief, 
                  MAXIT = 10,
                  # Folders to look in for large versioned files
                  look_in = 'release;source',
                  # Soft limits on file sizes
                  file_MB_limit = 2,
                  total_MB_limit = 500)
Depends(debrief, BUILD_TARGETS)
env.AlwaysBuild(debrief)
if 'state_of_repo.log' not in BUILD_TARGETS: 
    BUILD_TARGETS.append('state_of_repo.log')

atexit.register(log.end_log)


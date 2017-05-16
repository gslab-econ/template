# Preliminaries
import os
import sys
sys.dont_write_bytecode = True # Don't write .pyc files

# Test for proper prerequisites and setup
from configuration_test import configuration_test
[mode, sf, cache_dir] = configuration_test(ARGUMENTS, 
                                           gslab_python_version = '3.0.5')
import gslab_scons as gs
import gslab_scons.log as log
import yaml
import atexit

# Start log after getting mode and release version
mode = ARGUMENTS.get('mode', 'develop') 
vers = ARGUMENTS.get('version', '') 
log.start_log(mode, vers)

# Define the SCons environment
env = Environment(ENV = {'PATH' : os.environ['PATH']}, 
                  IMPLICIT_COMMAND_DEPENDENCIES = 0,
                  BUILDERS = {'Tablefill':   Builder(action = gs.build_tables),
                              'BuildLyx':    Builder(action = gs.build_lyx),
                              'BuildStata':  Builder(action = gs.build_stata),
                              'BuildPython': Builder(action = gs.build_python)},
                  user_flavor = sf)

# Only computes hash if time-stamp changed
env.Decider('MD5-timestamp') 
# Extensions to be used when scanning for source files in BuildLyx.
env.EXTENSIONS = ['.eps', '.pdf', '.lyx']
SourceFileScanner.add_scanner('.lyx', Scanner(gs.misc.lyx_scan, recursive = True))

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
debrief = Command('state_of_repo.log', [], gs.misc.scons_debrief, 
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

# Prevent the state-of-the-repo log from being pulled from cache
# rather than recreated as a part of each SCons run.
NoCache('state_of_repo.log')

atexit.register(log.end_log)

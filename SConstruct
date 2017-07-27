# Preliminaries
import os
import sys
sys.dont_write_bytecode = True # Don't write .pyc files

# Test for proper prerequisites and setup
from configuration_test import configuration_test
[mode, stata_executable, cache_dir] = configuration_test(ARGUMENTS, 
                                                     gslab_python_version = '4.0.0')
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
                  stata_executable = stata_executable)

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

debrief_env = {'MAXIT' : 10,
               # Folders to look in for large versioned files
               'look_in' : 'release;source',
               # Soft limits on file sizes
               'file_MB_limit' : 2,
               'total_MB_limit' : 500}
atexit.register(log.end_log)
atexit.register(gs.misc.scons_debrief, target = 'state_of_repo.log', env = debrief_env)

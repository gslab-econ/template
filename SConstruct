# Preliminaries
import os
import sys
import gslab_scons
mode = ARGUMENTS.get('mode', 'develop') # Gets mode; defaults to 'develop'

# Sets up logs and checks mode/version
if not (mode in ['develop', 'cache']):
	print("Error: %s is not a defined mode" % mode)
	sys.exit()

gslab_scons.start_log() 

# Defines environment
env = Environment(ENV = {'PATH' : os.environ['PATH']}, 
                  IMPLICIT_COMMAND_DEPENDENCIES = 0,
                  BUILDERS = {'Tablefill': Builder(action = gslab_scons.build_tables),
                              'Lyx'      : Builder(action = gslab_scons.build_lyx),
                              'R'        : Builder(action = gslab_scons.build_r),
                              'Stata'    : Builder(action = gslab_scons.build_stata)},
                  user_flavor = ARGUMENTS.get('sf', 'StataMP'))

env.Decider('MD5-timestamp') # Only computes hash if time-stamp changed
Export('env')

# Run sub-trees
SConscript('source/data/SConscript') 

# Additional mode options
if mode is 'cache':
	# Defines cache in cache mode
	USER        = os.environ['USER']
	local_cache = '/Users/%s/Google Drive/cache/large_template' % USER
	os.system('mkdir -p "%s"' % local_cache)
	CacheDir(local_cache)

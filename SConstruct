# Preliminaries
import os
import sys
import gslab_scons
mode = ARGUMENTS.get('mode', 'develop') # Gets mode; defaults to 'develop'
vers = ARGUMENTS.get('version', '') # Gets release version; defaults to ''

gslab_scons.start_log(mode, vers) # Sets up logs and checks mode/version


# Defines environment
env = Environment(ENV = {'PATH' : os.environ['PATH']}, 
				 IMPLICIT_COMMAND_DEPENDENCIES = 0,
				 BUILDERS = { 'Tablefill' : Builder(action = gslab_scons.build_tables),
                  			  'Lyx'       : Builder(action = gslab_scons.build_lyx),
                  			  'R'         : Builder(action = gslab_scons.build_r),
                  			  'Stata'     : Builder(action = gslab_scons.build_stata)})

env.Decider('MD5-timestamp') # Only computes hash if time-stamp changed
Export('env')

# Run sub-trees
SConscript('source/data/SConscript') 

# Additional mode options
if mode in ['cache', 'release']:
	# Defines cache in cache mode
	USER        = os.environ['USER']
	local_cache = '/Users/%s/Google Drive/cache/large_template' % USER
	os.system('mkdir -p "%s"' % local_cache)
	CacheDir(local_cache)

if mode == 'release':
	# Installs files appropirate locations in release mode
	local_release = '/Users/%s/Google Drive/release/large_template/' % USER
	local_release = local_release + vers + '/'
	DriveReleaseFiles = ['#build/data/data.txt']
	gslab_scons.Release(env, vers, DriveReleaseFiles, local_release)



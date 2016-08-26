import os
import sys
import gslab_scons
gslab_scons.start_log()

USER        = os.environ['USER']
local_cache = '/Users/%s/Google Drive/cache/large_template' % USER
os.system('mkdir -p "%s"' % local_cache)

env = Environment(ENV = {'PATH' : os.environ['PATH']}, 
				 IMPLICIT_COMMAND_DEPENDENCIES = 0,
				 BUILDERS = { 'Tablefill' : Builder(action = gslab_scons.build_tables),
                  			  'Lyx'       : Builder(action = gslab_scons.build_lyx),
                  			  'R'         : Builder(action = gslab_scons.build_r),
                  			  'Stata'     : Builder(action = gslab_scons.build_stata)})

env.Decider('MD5-timestamp') # Only computes hash if time-stamp changed
CacheDir(local_cache)
Export('env')

SConscript('source/data/SConscript') 



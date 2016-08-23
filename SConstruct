import os, sys
import gslab_scons
env = Environment(ENV = {'PATH' : os.environ['PATH']}, 
				 IMPLICIT_COMMAND_DEPENDENCIES = 0,
				 BUILDERS = { 
                              'Log'       : Builder(action = gslab_scons.build_log),
				              'Tablefill' : Builder(action = gslab_scons.build_tables),
                  			  'Lyx'       : Builder(action = gslab_scons.build_lyx),
                  			  'R'         : Builder(action = gslab_scons.build_r),
                  			  'Stata'     : Builder(action = gslab_scons.build_stata)})

env.Decider('MD5-timestamp') # Only computes hash if time-stamp changed
Export('env')

SConscript('source/data/SConscript') 
SConscript('source/analysis/SConscript')
SConscript('source/paper/SConscript') 
SConscript('source/talk/SConscript') 


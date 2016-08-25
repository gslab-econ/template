import os
import sys
import gslab_scons
gslab_scons.start_log()

env = Environment(ENV = {'PATH' : os.environ['PATH']}, 
				 IMPLICIT_COMMAND_DEPENDENCIES = 0,
				 BUILDERS = { 'Tablefill' : Builder(action = gslab_scons.build_tables),
                  			  'Lyx'       : Builder(action = gslab_scons.build_lyx),
                  			  'R'         : Builder(action = gslab_scons.build_r),
                  			  'Stata'     : Builder(action = gslab_scons.build_stata)})

# Set Stata flavour here
env.Append(stata_flavour = 'StataMP')

env.Decider('MD5-timestamp') # Only computes hash if time-stamp changed
Export('env')

SConscript('source/data/SConscript') 
SConscript('source/analysis/SConscript')
SConscript('source/paper/SConscript') 
SConscript('source/talk/SConscript') 


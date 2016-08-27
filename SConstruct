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

# Set Stata flavor here, syntax:  `scons --sf=StataMP`
AddOption('--sf', 
          type    = 'string',
          nargs   = 1,
          dest    = 'flavor_input',
          action  = 'store',
          help    = 'Provide Stata flavour between "StataMP", "StataSE", or "Stata"',
          default = None)
env.Append(user_flavor = GetOption('flavor_input'))

env.Decider('MD5-timestamp') # Only computes hash if time-stamp changed
Export('env')

SConscript('source/data/SConscript') 
SConscript('source/analysis/SConscript')
SConscript('source/paper/SConscript') 
SConscript('source/talk/SConscript') 


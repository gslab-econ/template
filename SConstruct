import os
import sys
import gslab_scons.build as build
import gslab_scons.log as log

log.start_log()

env = Environment(ENV = {'PATH' : os.environ['PATH']}, 
                  IMPLICIT_COMMAND_DEPENDENCIES = 0,
                  BUILDERS = { 'Tablefill' : Builder(action = build.build_tables),
                               'Lyx'       : Builder(action = build.build_lyx),
                               'R'         : Builder(action = build.build_r),
                               'Stata'     : Builder(action = build.build_stata)},
                  user_flavor = ARGUMENTS.get('sf', 'StataMP'))


env.Decider('MD5-timestamp') # Only computes hash if time-stamp changed
Export('env')

SConscript('source/data/SConscript') 
SConscript('source/analysis/SConscript')
SConscript('source/paper/SConscript') 
SConscript('source/talk/SConscript') 

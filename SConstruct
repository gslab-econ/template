
import os
import sys
import gslab_scons.builders as build
import gslab_scons.log as log

mode = ARGUMENTS.get('mode', 'develop') # Gets mode; defaults to 'develop'
vers = ARGUMENTS.get('version', '') # Gets release version; defaults to ''
log.start_log(mode, vers)

env = Environment(ENV = {'PATH' : os.environ['PATH']}, 
                  IMPLICIT_COMMAND_DEPENDENCIES = 0,
                  BUILDERS = { 'Tablefill' : Builder(action = build.build_tables),
                               'Lyx'       : Builder(action = build.build_lyx),
                               'R'         : Builder(action = build.build_r),
                               'Stata'     : Builder(action = build.build_stata)},
                  user_flavor = ARGUMENTS.get('sf', None))


env.Decider('MD5-timestamp') # Only computes hash if time-stamp changed
Export('env')

SConscript('source/data/SConscript') 
SConscript('source/analysis/SConscript')
SConscript('source/paper/SConscript') 
SConscript('source/talk/SConscript') 
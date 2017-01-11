
import os
import re
import sys
import time
import gslab_scons.builders as build
import gslab_scons.log as log
from gslab_scons.misc import state_of_repo

log.start_log()

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


# Print the state of the repo at end of SCons run
finish_command = Command( 'state_of_repo', [], state_of_repo ) # From http://stackoverflow.com/questions/8901296/how-do-i-run-some-code-after-every-build-in-scons
Depends(finish_command, BUILD_TARGETS)
if 'state_of_repo' not in BUILD_TARGETS: 
	BUILD_TARGETS.append('state_of_repo')
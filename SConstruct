import os

env = Environment(IMPLICIT_COMMAND_DEPENDENCIES = 0)
env.Decider('MD5-timestamp') # Only computes hash if time-stamp changed
Export('env')

SConscript('source/data/SConscript')
SConscript('source/analysis/SConscript')



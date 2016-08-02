import os

env = Environment()
env.Decider('MD5-timestamp') # Only computes hash if time-stamp changed
Export('env')

SConscript('source/data/Sconscript')
SConscript('source/analysis/Sconscript')



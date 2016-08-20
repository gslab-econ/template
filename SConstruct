import os, sys
sys.stdout = os.popen("tee sconstruct_out.log", "w")
sys.stderr = os.popen("tee sconstruct_err.log", "w")

env = Environment(ENV = {'PATH' : os.environ['PATH']}, 
					IMPLICIT_COMMAND_DEPENDENCIES = 0)
env.Decider('MD5-timestamp') # Only computes hash if time-stamp changed
Export('env')

SConscript('source/data/SConscript') 
SConscript('source/analysis/SConscript')
SConscript('source/paper/SConscript') 
SConscript('source/talk/SConscript') 

os.system('cat sconstruct_out.log  > sconstruct.log')
Install('./output', 'sconstruct.log')

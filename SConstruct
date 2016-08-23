import os, sys
sys.stdout = os.popen("tee sconstruct.log", "w")
sys.stderr = sys.stdout 

env = Environment(ENV = {'PATH' : os.environ['PATH']}, 
					IMPLICIT_COMMAND_DEPENDENCIES = 0)
env.Decider('MD5-timestamp') # Only computes hash if time-stamp changed
Export('env')

SConscript('source/data/SConscript') 
SConscript('source/analysis/SConscript')
SConscript('source/paper/SConscript') 
SConscript('source/talk/SConscript') 

Ignore("./output", "sconstruct.log")
Command(
	target = "./output", 
	source = "sconstruct.log", 
	action = [
	           env.Install("$TARGET", "$SOURCE"),  
	           Delete("$SOURCE")
	         ]
)

# env.Install('./output', 'sconstruct.log')

# env.Command(
# 	target = "sconstruct.log", 
# 	source = [], 
# 	action = "rm $TARGET"
# )

# Execute(Delete('sconstruct.log'))

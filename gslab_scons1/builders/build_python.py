import os
import gslab_scons1.misc as misc
from gslab_scons1 import log_timestamp

def build_python(target, source, env):
    '''Build SCons targets using a Python script

    This function executes a Python script to build objects specified
    by target using the objects specified by source.

    Parameters
    ----------
    target: string or list 
        The target(s) of the SCons command.
    source: string or list
        The source(s) of the SCons command. The first source specified
        should be the Python script that the builder is intended to execute. 
    '''
    source      = misc.make_list_if_string(source)
    target      = misc.make_list_if_string(target)
    start_time  = misc.current_time()
    source_file = str(source[0])
    target_file = str(target[0])
    target_dir  = os.path.dirname(target_file)
    misc.check_code_extension(source_file, 'python')
    log_file    = target_dir + '/sconscript.log'
    cl_arg      = misc.command_line_arg(env)

    os.system('python %s %s > %s' % (source_file, cl_arg, log_file))

    end_time   =  misc.current_time()    
    log_timestamp(start_time, end_time, log_file)
    return None

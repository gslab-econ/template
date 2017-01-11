import os
import subprocess
import shutil
import gslab_scons1.misc as misc
from gslab_scons1 import log_timestamp
from gslab_scons1._exception_classes import BadExecutableError
from sys import platform

def build_stata(target, source, env):
    '''Build targets with a Stata command
 
    This function executes a Stata script to build objects specified
    by target using the objects specified by source.

    Parameters
    ----------
    target: string or list 
        The target(s) of the SCons command.
    source: string or list
        The source(s) of the SCons command. The first source specified
        should be the Stata .do script that the builder is intended to execute. 

    Note: the user can specify a flavour by typing `scons sf=StataMP` 
    (By default, SCons will try to find each flavour). 
    '''
    start_time =  misc.current_time()
    cl_arg     = misc.command_line_arg(env)

    source       = misc.make_list_if_string(source)
    target       = misc.make_list_if_string(target)
    source_file  = str(source[0])
    target_file  = str(target[0])

    target_dir   = os.path.dirname(target_file)
    misc.check_code_extension(source_file, 'stata')
    log_file = target_dir + '/sconscript.log'
    loc_log  = os.path.basename(source_file).replace('.do','.log')

    user_flavor  = env['user_flavor']  
    if user_flavor is not None:
        if misc.is_unix():
            command = misc.stata_command_unix(user_flavor, cl_arg)
        elif platform == 'win32':
            command = misc.stata_command_win(user_flavor, cl_arg)
    else:
        flavors = ['stata-mp', 'stata-se', 'stata']
        if misc.is_unix():
            for flavor in flavors:
                if misc.is_in_path(flavor):
                    command = misc.stata_command_unix(flavor, cl_arg)
                    break
        elif platform == 'win32':
            try:
                key_exist = os.environ['STATAEXE'] is not None
                command   = misc.stata_command_win("%%STATAEXE%%")
            except KeyError:
                flavors = [(f.replace('-', '') + '.exe') for f in flavors]
                if misc.is_64_windows():
                    flavors = [f.replace('.exe', '-64.exe') for f in flavors]
                for flavor in flavors:
                    if misc.is_in_path(flavor):
                        command = misc.stata_command_win(flavor, cl_arg)
                        break

    try:
        subprocess.check_output(command % source_file, 
                                stderr = subprocess.STDOUT,
                                shell  = True)
    except subprocess.CalledProcessError:
        raise BadExecutableError('Could not find executable.')

    shutil.move(loc_log, log_file)
    end_time = misc.current_time()
    log_timestamp(start_time, end_time, log_file)
    return None

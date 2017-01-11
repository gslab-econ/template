import os
import shutil
import gslab_scons.misc as misc
from gslab_scons import log_timestamp
from gslab_scons._exception_classes import BadExecutableError


def build_lyx(target, source, env):
    '''Compile a pdf from a LyX file

    This function is a SCons builder that compiles a .lyx file
    as a pdf and places it at the path specified by target. 

    Parameters
    ----------
    target: string or list 
        The target of the SCons command. This should be the path
        of the pdf that the builder is instructed to compile. 
    source: string or list
        The source of the SCons command. This should
        be the .lyx file that the function will compile as a PDF.

    '''
    source      = misc.make_list_if_string(source)
    target      = misc.make_list_if_string(target)
    start_time  = misc.current_time()
    source_file = str(source[0])
    target_file = str(target[0])
    target_dir  = os.path.dirname(target_file)
    misc.check_code_extension(source_file, 'lyx')
    newpdf      = source_file.replace('.lyx','.pdf')
    log_file    = target_dir + '/sconscript.log'
    
    os.system('lyx -e pdf2 %s > %s' % (source_file, log_file))
    
    shutil.move(newpdf, target_file)
    end_time    = misc.current_time()
    log_timestamp(start_time, end_time, log_file)
    return None

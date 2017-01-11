import gslab_scons1.misc as misc
from gslab_fill import tablefill


def build_tables(target, source, env):
    '''Build a SCons target by filling a table

    This function uses the tablefill function from gslab_fill to produced a 
    filled table from (i) an empty table in a LyX file and (ii) text files 
    containing data to be used in filling the table. 

    Parameters
    ----------
    target: string or list 
        The target(s) of the SCons command.
    source: string or list
        The source(s) of the SCons command. The first source specified
        should be the LyX file specifying the table format. The subsequent 
        sources should be the text files containing the data with which the
        tables are to be filled. 
    '''
    source = misc.make_list_if_string(source)
    target = misc.make_list_if_string(target)
    
    misc.check_code_extension(str(target[0]), 'lyx')
    
    tablefill(input    = ' '.join([str(a) for a in source[1:len(source)]]), 
              template = str(source[0]), 
              output   = str(target[0]))
    return None

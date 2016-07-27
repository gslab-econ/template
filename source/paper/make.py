#! /usr/bin/env python
#****************************************************
# GET LIBRARY
#****************************************************
import subprocess, shutil, os
gslab_make_path = os.getenv('gslab_make_path')
subprocess.call('svn export --force -r 33345 ' + gslab_make_path + ' gslab_make', shell = True)
from gslab_make.py.get_externals import *
from gslab_make.py.make_log import *
from gslab_make.py.run_program import *
from gslab_make.py.dir_mod import *

#****************************************************
# MAKE.PY STARTS
#****************************************************

# SET OPTIONS
set_option(makelog = '../../output/paper/make.log', 
	    output_dir = '../../output/paper/', 
	      temp_dir = '', 
	  external_dir = '../../external/paper/')
clear_dirs('../../external/paper/', '../../output/paper/')
start_make_logging('../../output/paper/make.log')

# GET_EXTERNALS
get_externals('./externals.txt')
sys.path.append('../../external/paper/lib/python/')
from gslab_misc.py.tablefill import tablefill
from gslab_misc.py.textfill import textfill

# COMPILE (ORDER MATTERS)
run_lyx(program = './paper.lyx')
run_lyx(program = './paper_online.lyx')
run_lyx(program = './claims.lyx')

end_make_logging('../../output/paper/make.log')

shutil.rmtree('gslab_make')
raw_input('\n Press <Enter> to exit.')

#! /usr/bin/env python
import subprocess, shutil, os
FROM_DIR = False
if (not os.path.exists('../../gslab_make')):
    FROM_DIR = True
    gslab_make_path = os.getenv('gslab_make_path')
    subprocess.call('svn export --force -r 33345 ' + gslab_make_path + ' gslab_make', shell = True)
    from gslab_make.py.get_externals import *
    from gslab_make.py.make_log import *
    from gslab_make.py.run_program import *
    from gslab_make.py.dir_mod import *

# SET OPTIONS
set_option(makelog = '../../output/paper/make.log', 
	    output_dir = '../../output/paper/', 
	      temp_dir = '', 
	  external_dir = '')
clear_dirs('../../output/paper/')
start_make_logging('../../output/paper/make.log')

# COMPILE (ORDER MATTERS)
run_lyx(program = './paper.lyx')
run_lyx(program = './paper_online.lyx')
run_lyx(program = './claims.lyx')

end_make_logging('../../output/paper/make.log')

if (FROM_DIR == True):
    shutil.rmtree('gslab_make')
    raw_input('\n Press <Enter> to exit.')
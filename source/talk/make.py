#! /usr/bin/env python
# Run this file from /source/talk/
#****************************************************
# GET LIBRARY
#****************************************************
import subprocess, shutil, os
gslab_make_path = os.getenv('gslab_make_path')
subprocess.call('svn export --force -r 33502 ' + gslab_make_path + ' gslab_make', shell = True)
from gslab_make.py.get_externals import *
from gslab_make.py.make_log import *
from gslab_make.py.run_program import *
from gslab_make.py.dir_mod import *

#****************************************************
# MAKE.PY STARTS
#****************************************************

set_option(makelog      = '../../output/talk/make.log', 
	       output_dir   = '../../output/talk/', 
	       temp_dir     = '../../temp/talk/', 
	       external_dir = '../../external/talk/')

clear_dirs('../../output/talk/', '../../temp/talk/', '../../external/talk/')
start_make_logging()

run_lyx(program = './slides.lyx')
run_lyx(program = './slides.lyx', 
	handout = True, 
	comments = True, 
	pdfout = '../../temp/talk/politext_handout.pdf')
end_make_logging()

shutil.rmtree('gslab_make')
input('\n Press <Enter> to exit.')


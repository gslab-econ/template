#! /usr/bin/env python
import subprocess, shutil, os
FROM_DIR = False
if (not os.path.exists('../../gslab_make')):
    FROM_DIR = True
    import subprocess, shutil, os
    gslab_make_path = os.getenv('gslab_make_path')
    subprocess.call('svn export --force -r 33345 ' + gslab_make_path + ' gslab_make', shell = True)
    from gslab_make.py.get_externals import *
    from gslab_make.py.make_log import *
    from gslab_make.py.run_program import *
    from gslab_make.py.dir_mod import *

set_option(makelog      = '../../output/talk/make.log', 
	       output_dir   = '../../output/talk/', 
	       temp_dir     = '../../output/talk/', 
	       external_dir = '')

clear_dirs('../../output/talk/')
start_make_logging()

run_lyx(program  = './slides.lyx')
run_lyx(program  = './slides.lyx', 
	    handout  = True, 
	    comments = True, 
	    pdfout   = '../../output/talk/talk_handout.pdf')
end_make_logging()

if (FROM_DIR == True):
    shutil.rmtree('gslab_make')
    raw_input('\n Press <Enter> to exit.')
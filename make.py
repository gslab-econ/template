execfile("lib/make/py/library.py")
gslab_make_path = os.getenv('gslab_make_path')
subprocess.call('svn export --force -r 33345 ' + gslab_make_path + ' gslab_make', shell = True)
from gslab_make.py.get_externals import *
from gslab_make.py.make_log import *
from gslab_make.py.run_program import *
from gslab_make.py.dir_mod import *

LOG = "./output/make.log"

if os.path.isfile(LOG):
	os.remove(LOG)

source_make("data", LOG)
source_make("analysis", LOG)
source_make("paper", LOG)
source_make("talk", LOG)

shutil.rmtree('gslab_make')
raw_input('\n Press <Enter> to exit.')
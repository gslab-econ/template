execfile("../../lib/make/py/library.py")
load_paths("PATHS_SOURCE", "paths.txt")
load_paths("PATHS_LIB", "../../lib/paths.txt")

USERNAME   = set_envir_var("USERNAME", "lboxell")
PASSWORD   = set_envir_var("PASSWORD", "W3d.nesday")
SVNROOT    = set_envir_var("SVNROOT", "https://econ-gentzkow-svn.stanford.edu/repos/main/trunk")
OUTPUT_DIR = os.environ["OUTPUT_DIR"]
DATA_DIR   = os.environ["DATA_DIR"]

clear_dir(OUTPUT_DIR)
clear_dir(DATA_DIR)

LOG = set_envir_var("LOG", OUTPUT_DIR + "/make.log")

os.system("echo 'Starting at ' $(date +%D:%H:%M:%S) >> " + LOG)

getSVN(USERNAME, PASSWORD, SVNROOT, 
       "/raw/StopWord Lists/data", 
       DATA_DIR,    
       OUTPUT_DIR + "/externals.log")
 
if (os.path.exists("../../raw/data/.svn")): 
    shutil.rmtree("../../raw/data/.svn")

run_R("process_stopwords.R",  LOG)

os.system("echo 'Finished at ' $(date +%D:%H:%M:%S) >> " + LOG)

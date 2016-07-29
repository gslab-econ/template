execfile("../../lib/make/py/library.py")

load_paths("PATHS_SOURCE", "paths.txt")
load_paths("PATHS_LIB", "../../lib/paths.txt")

clear_dir("OUTPUT_DIR", path = True)

LOG = set_envir_var("LOG", os.environ["OUTPUT_DIR"] + "/make.log")

run_R("sample_plots.R", LOG)
run_StataMP("sample_stata.do", LOG)

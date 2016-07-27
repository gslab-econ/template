execfile("lib/make/py/library.py")

load_paths("PATHS_SOURCE", "source/analysis/example/paths.txt")
load_paths("PATHS_LIB", "lib/paths.txt")

clear_dir("OUTPUT_DIR", path = True)

LOG = set_envir_var("LOG", os.environ["OUTPUT_DIR"] + "/make.log")

run_R("source/analysis/example/sample_plots.R", LOG)
run_StataMP("source/analysis/example/sample_stata.do", LOG)
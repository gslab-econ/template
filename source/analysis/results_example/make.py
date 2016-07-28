execfile("lib/make/py/library.py")

load_paths("PATHS_SOURCE", "source/analysis/results_example/paths.txt")
load_paths("PATHS_LIB", "lib/paths.txt")

clear_dir("OUTPUT_DIR", path = True)
clear_dir("RESULTS_DIR", path = True)

LOG = set_envir_var("LOG", os.environ["OUTPUT_DIR"] + "/make.log")

run_R("source/analysis/results_example/generate_wordlists.R", LOG)


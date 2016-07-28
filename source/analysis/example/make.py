from bld.project_paths import project_paths_join as ppj
execfile(ppj("MAKE_LIB", "library.py"))
clear_dir(ppj("OUT_EXAMPLE"))


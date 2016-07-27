paths_lists <- Sys.getenv()[grep("^PATHS", names(Sys.getenv()))]

for (path in paths_lists) {
    path_names <- read.table(path)[1]
    
    for (name in levels(as.vector(path_names)[, 1])) {
        name <- toString(name)
        assign(name, Sys.getenv(name))
    }
}

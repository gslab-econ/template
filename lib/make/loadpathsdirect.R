
LoadPathsDirect <- function(additionalPath = "",
                         standardPaths = c("output/data/paths.txt",
                                          "lib/paths.txt")) {
    
    paths_list <- c(additionalPath, standardPaths)
    paths_list <- paths_list[paths_list != ""]
    
    for (path in paths_list) {
      
        path_names  <- unlist(read.table(path, as.is = T)[1])
        path_values <- unlist(read.table(path, as.is = T)[2])
        
        for (i in 1:length(path_names)) {
            name  <- toString(path_names[i])
            value <- toString(path_values[i])
            assign(name, value, envir = .GlobalEnv)
        }
      
    }

}
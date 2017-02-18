library(yaml)
PATHS <- yaml.load_file('constants.yaml')
args  <- commandArgs(TRUE)

main <- function(i){
    x    <- seq(-10, 10, 0.1)
    write.table(x, sprintf("%s/%s.txt", PATHS$build$data, i), sep = "|", 
                   row.names = FALSE, col.names = TRUE, quote = FALSE) 
}

main(args[1])

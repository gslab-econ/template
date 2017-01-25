args = commandArgs(TRUE)

main <- function(i){
    x    <- seq(-10, 10, 0.1)
    write.table(x, sprintf("build/data/data_%s.txt", i), sep = "|", 
    				row.names = FALSE, col.names = TRUE, quote = FALSE) 
}

main(args[1])

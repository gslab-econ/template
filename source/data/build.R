args = commandArgs(TRUE)

main <- function(i){
    x    <- seq(-10, 10, 0.1)
    write.table(x, sprintf("output/data/data_%s.txt", i), sep = "|", row.names = FALSE, col.names = FALSE) 
}

main(args[1])
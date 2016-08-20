main <- function(){
    x    <- seq(-10, 10, 0.2)
    write.table(x, "output/data/data.txt", sep = "|", row.names = FALSE, col.names = FALSE) 
}

main()
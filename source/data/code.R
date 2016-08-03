main <- function(){
    x    <- seq(-10, 10, 0.1)
    exp  <- exp(x)
    quad <- sapply(x, function(z) z**2)
    data <- data.frame(x, exp, quad)
    write.table(data, "output/data/data.txt", sep = "|", row.names = FALSE, col.names = TRUE) 
}

main()
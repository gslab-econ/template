x <- seq(-13, 100, 0.1)
write.table(x, "build/data/data.txt", sep = "|", row.names = FALSE, col.names = FALSE)

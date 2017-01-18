set.seed(1)
x <- sample(1:10, 1000, replace = T)
write.table(x, "output/data/data.txt", sep = "|", row.names = FALSE, col.names = TRUE, quote = FALSE)

Main <- function(){
  word        <- readLines("data/raw/stopWords_Fox.txt")
  len          <- sapply(word, nchar)
  word_lengths <- data.frame(word, len)
  write.csv(x    = word_lengths, 
            file = "data/derived/stopWords_Fox_lengths.csv",
            row.names = FALSE)
}

Main()
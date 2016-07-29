Main <- function(){
  
    DATA_DIR   <- Sys.getenv("DATA_DIR")
    OUTPUT_DIR <- Sys.getenv("OUTPUT_DIR")
  
    data_file    <- sprintf("%s/stopWords_Fox.txt", DATA_DIR)
    output_file  <- sprintf("%s/stopWords_Fox_lengths.csv", OUTPUT_DIR)
    
    word         <- readLines(data_file)
    len          <- sapply(word, nchar)
    word_lengths <- data.frame(word, len)
    write.csv(x    = word_lengths, 
              file = output_file,
              row.names = FALSE)
}

Main()
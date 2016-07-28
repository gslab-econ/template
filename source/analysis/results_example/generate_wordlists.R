Main <- function(){
    set.seed(100)

    DATA_DIR    <- Sys.getenv("DATA_DIR")
    RESULTS_DIR <- Sys.getenv("RESULTS_DIR")

    print(DATA_DIR)    
    print(RESULTS_DIR)

    stopwords      <- read.csv(sprintf("%s/stopWords_Fox_lengths.csv", DATA_DIR))
    stopwords$word <- as.character(stopwords$word)

    # Only use words that are longer than one character
    stopwords <- stopwords[which(stopwords$len > 1), ]

    # Create 10 lists of one thousand randomly selected (with replacement) stopwords
    for (n in 0:9){
        wordlist <- sample(x       = stopwords$word, 
        	               size    = 1000,
        	               replace = TRUE)
        writeLines(text = wordlist, 
        	       con  = sprintf("%s/wordlist%d.txt", RESULTS_DIR, n))
    }
}

Main()
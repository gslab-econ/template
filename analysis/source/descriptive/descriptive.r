library(yaml)

main <- function() {
    PATHS <- yaml.load_file("config_global.yaml")
    data  <- read.table(sprintf("%s/data.txt", PATHS$build$prepare_data), header = TRUE)
    
    sink(sprintf("%s/table_r.txt", PATHS$build$descriptive))
    cat("<tab:table>\n")
    cat(sprintf("%s\n%.3f\n%d\n%d",
               mean(data$x), sd(data$x), max(data$x), min(data$x)))
    sink()

    postscript(sprintf("%s/plot_r.eps", PATHS$build$descriptive))
    hist(data$x, breaks = 10)
    dev.off()
}

main()

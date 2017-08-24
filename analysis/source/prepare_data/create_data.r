library(yaml)
PATHS <- yaml.load_file("config_global.yaml")

main <- function() {
    x <- 1:300000
    write.table(x, sprintf("%s/data_r.txt", PATHS$build$prepare_data),
                row.names = FALSE, col.names = TRUE, quote = FALSE)
}
main()


library(yaml)
CONFIG <- yaml.load_file("config_global.yaml")

main <- function() {
    x <- 1:300000
    write.table(x, sprintf("%s/data.txt", CONFIG$build$prepare_data),
                row.names = FALSE, col.names = TRUE, quote = FALSE)
}
main()


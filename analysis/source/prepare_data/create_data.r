library(yaml)
paths_global <- yaml.load_file("config_global.yaml")

main <- function() {
    x <- 1:300000
    write.table(x, sprintf("%s/data.txt", paths_global$build$prepare_data),
                row.names = FALSE, col.names = TRUE, quote = FALSE)
}
main()


library(yaml)
CONFIG <- yaml.load_file("config_global.yaml")
build_path <- CONFIG$build$prepare_data


main <- function() {
    x <- 1:300000
    write.table(x, sprintf("%s/data.txt", build_path),
                row.names = FALSE, col.names = TRUE, quote = FALSE)
}
main()


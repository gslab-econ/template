# Required packages installed from CRAN.
CRAN_packages   <- c("yaml")
# Required packages installed from Github. Should be the full path to the relevant repo.
GitHub_packages <- NULL

main <- function(CRAN_packages = NULL, GitHub_packages = NULL) {
    # If there are packages installed from Github, first make sure "devtools" is installed 
    if (!is.null(GitHub_packages)) {
        CRAN_packages <- c(CRAN_packages, "devtools")
    }

    # Install packages from CRAN
    if (!is.null(CRAN_packages)) {
        lapply(CRAN_packages, install_CRAN, repo = "http://cran.cnr.Berkeley.edu/",
                              dependency = TRUE, quiet = TRUE)
    }

    # Install packages from GitHub
    if (!is.null(GitHub_packages)) {
        library(devtools)
        lapply(GitHub_packages, function(pkg) install_github(pkg))
    }
}

install_CRAN <- function(pkg, repo, dependency, quiet){
    if (system.file(package = pkg) == "") {
        install.packages(pkg, repos = repo, dependencies = dependency, quiet = quiet)
    }
}

main(CRAN_packages, GitHub_packages)

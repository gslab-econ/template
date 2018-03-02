# *** Add required packages from CRAN to this list ***
CRAN_packages   <- c("yaml")
# *** Add required packages from CRAN to this list ***

# *** Add required packages from GitHub (UserName/RepositoryName) to this vector ***
GitHub_packages <- NULL
# *** Add required packages from GitHub (UserName/RepositoryName) to this vector ***

main <- function(CRAN_packages = NULL, GitHub_packages = NULL,
                 CRAN_repo = "http://cran.cnr.Berkeley.edu/",
                 dependency = TRUE, quiet = TRUE, upgrade = FALSE) {
    # If there are packages installed from Github, first make sure "devtools" is installed 
    if (!is.null(GitHub_packages)) {
        CRAN_packages <- c(CRAN_packages, "devtools")
    }

    # Install packages from CRAN
    if (!is.null(CRAN_packages)) {
        lapply(CRAN_packages, install_CRAN, repo = CRAN_repo, dependency = dependency,
               quiet = quiet, upgrade = upgrade)
    }

    # Install packages from GitHub
    if (!is.null(GitHub_packages)) {
        library(devtools)
        lapply(GitHub_packages, function(pkg) install_github(pkg))
    }
}

install_CRAN <- function(pkg, repo, dependency, quiet, upgrade = FALSE) {
    if (upgrade) {
        install.packages(pkg, repos = repo, dependencies = dependency, quiet = quiet)
    } else {
        if (system.file(package = pkg) == "") {
            install.packages(pkg, repos = repo, dependencies = dependency, quiet = quiet)
        }
    }
}

# upgrade = TRUE will update all packages to the most current version
# upgrade = FALSE will skip packages that are already installed
main(CRAN_packages, GitHub_packages, upgrade = FALSE)

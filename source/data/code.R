main <- function(){  
	source("project_paths.r") ## This is how waf controls paths -- it creates a file that lists all the "Environment" variables/paths (they aren't system environment variables, but more like 'waf' environment variables)
    x    <- seq(-10, 10, 0.1)
    exp  <- exp(x)
    quad <- sapply(x, function(z) z**2)
    data <- data.frame(x, exp, quad)
    saveRDS(data, sprintf("%s/data.rds", PATH_OUT_DATA))
}

main()
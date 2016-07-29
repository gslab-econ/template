Main <- function(){
    source("project_paths.r")
    library(lattice)

	data <- readRDS(sprintf("%s/data.rds", PATH_OUT_DATA))
    
    lin_plot  <- xyplot(x    ~ x, data, type = 'l', ylab = 'y')
    exp_plot  <- xyplot(exp  ~ x, data, type = 'l', ylab = 'y')
    quad_plot <- xyplot(quad ~ x, data, type = 'l', ylab = 'y')
    
    print("This is a sample message for the log.")
    
    SavePlot(lin_plot,  "plot", PATH_OUT_EXAMPLE)
    SavePlot(exp_plot,  "appendix_plot", PATH_OUT_EXAMPLE)
    SavePlot(quad_plot, "online_plot", PATH_OUT_EXAMPLE)
}

SavePlot <- function(plot,  filename, dir){
    pdf(sprintf("%s/%s.pdf", dir, filename))
    print(plot)
    dev.off()
}

Main()
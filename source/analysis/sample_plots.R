Main <- function(){
    library(lattice)
    OUTPUT_DIR <- "output/analysis"

    data <- readRDS("output/data/data.rds")
    
    lin_plot  <- xyplot(x    ~ x, data, type = 'l', ylab = 'y')
    exp_plot  <- xyplot(exp  ~ x, data, type = 'l', ylab = 'y')
    quad_plot <- xyplot(quad ~ x, data, type = 'l', ylab = 'y')
    
    print("This is a sample message for the log.")
    
    SavePlot(lin_plot,  "plot", OUTPUT_DIR)
    SavePlot(exp_plot,  "appendix_plot", OUTPUT_DIR)
    SavePlot(quad_plot, "online_plot", OUTPUT_DIR)
}

SavePlot <- function(plot,  filename, OUTPUT_DIR){
    pdf(sprintf("%s/%s.pdf", OUTPUT_DIR, filename))
    print(plot)
    dev.off()
}

Main()
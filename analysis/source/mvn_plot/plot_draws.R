#### Plot draws obtained from a multivariate normal distribution
# make sure to set directory to analysis folder - setwd("analysis") if it is not already
library(yaml)
library(tidyverse)
CONFIG <- yaml.load_file("config_global.yaml")

# read in csv file of 1000 random draws from multivariate normal dstr
draws <- read.csv(file = sprintf("%s/mvn_draws.csv", CONFIG$build$mvn_draws))

# plot data in any creative ways
plot <-
  ggplot(
    data = draws,
    aes(x = V1, y = V2)
    ) + 
  geom_point(alpha = 0.5) + 
  labs(x = "x", y = "y", title = "1000 Draws from a Bivariate Normal Distribution")
ggsave(sprintf("%s/mvn_plot.pdf", CONFIG$build$mvn_plot))

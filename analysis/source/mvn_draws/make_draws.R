#### Simulate 1000 draws from a Multivariate Normal Distribution ####
library(MASS)
library(yaml)
CONFIG <- yaml.load_file("config_global.yaml")

## Bivariate case
# set mean & covariance matrix
mu <- c(0,0)
sig <- matrix(c(1, .5, .5, 1), 2) 

# draw from distribution with parameters set above
draws <- mvrnorm(n = 1000, mu = mu, Sigma = sig, tol = 1e-06, empirical = FALSE)

# save data into .csv
write.csv(draws, sprintf("%s/mvn_draws.csv", CONFIG$build$mvn_draws))


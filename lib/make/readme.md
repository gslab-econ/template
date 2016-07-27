### Overview

This directory houses auxiliary scripts for code execution. 


### Code descriptions

 - `loadpaths.sh` loads a set of environment variables as defined in a `paths.txt` file into the shell environment 
 - `loadpaths.R` loads a set of environment variables as defined in a `paths.txt` file into the R environment.
 - `loadpathsdirect.R` is an alternative to `loadpaths.R`, useful when developing outside of the shell (e.g., in Rstudio) and the variables being loaded are not defined in the shell's environment space.  
 
### Notes

For an example of a well-defined `paths.txt` file see `./test/paths.txt`.

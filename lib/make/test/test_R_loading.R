
# function testing whether variable is defined and value is correct
TestVarDefined <- function(name, value, varsLoaded){
  
  if (name %in% varsLoaded) {
    cat(sprintf("PASS: %s defined.\n", name))
    
    if (value == get(name)) {
      cat(sprintf("PASS: %s defined at correct value.\n", name))
    } else {
      cat(sprintf("FAIL: %s defined at incorrect value.\n", name))
    }
    
  } else {
    cat(sprintf("FAIL: %s not defined.\n", name))
    cat(sprintf("FAIL: %s no value.\n", name))
  }
}

# Run load paths script
source(Sys.getenv("LOADPATHS_R"))

# Get names of variables loaded into session
varsLoaded <- ls()

# Define correct names and values for comparison (these are those in paths.txt)
varNames   <- c("VAR1", "VAR2", "VERYVERYVERYLONGVARNAME3")
varValues  <- c("value1", "veryLongValue2", "value3With!@#%^^&*()")

# Run
for (i in 1:length(varNames)) {
  name_i  <- varNames[i]
  value_i <- varValues[i]
  TestVarDefined(name_i, value_i, varsLoaded)
}





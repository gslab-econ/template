#!/bin/bash

# Start logging

export LOG=lib/make/test/test.log
rm -f $LOG

# assumes run from root of politext repo
export PATHS=lib/make/test/paths.txt
source lib/make/loadpaths.sh $PATHS >> $LOG
export LOADPATHS_R=lib/make/loadpaths.R

# Test correct definition in shell
if [ $VAR1 == "value1" ]; then
	echo "PASS: VAR1 defined properly." >> $LOG
else 
	echo "FAIL: VAR1 not defined properly." >> $LOG
fi

if [ $VAR2 == "veryLongValue2" ]; then
	echo "PASS: VAR2 defined properly." >> $LOG
else 
	echo "FAIL: VAR2 not defined properly." >> $LOG	
fi

if [ $VERYVERYVERYLONGVARNAME3 == "value3With!@#%^^&*()" ]; then
	echo "PASS: VERYVERYVERYLONGVARNAME3 defined properly." >> $LOG
else 
	echo "FAIL: VERYVERYVERYLONGVARNAME3 not defined properly." >> $LOG	
fi


# Test correct definition of variables in R
Rscript lib/make/test/test_R_loading.R >> $LOG

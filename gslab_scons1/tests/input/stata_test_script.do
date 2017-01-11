version 12
set more off
adopath + ../external/lib/stata/gslab_misc/ado/
preliminaries

set obs 10
gen var1 = _n

save_data ../output/stata1.dta, key(var1) log(../output/data_file_manifest.log) replace
save_data ../output/stata2.dta, key(var1) log(../output/data_file_manifest.log) replace
save_data ../output/stata.csv, key(var1) outsheet log(../output/data_file_manifest.log) replace
save_data ../output/stata.txt, key(var1) outsheet log(../output/data_file_manifest.log) replace

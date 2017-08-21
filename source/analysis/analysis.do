version 14
clear all
set more off

program main
    yaml read YAML using constants.yaml
    yaml local build_analysis=YAML.build.analysis

    set obs 20
    egen x = fill(1 2 3 4 5 6 7 8)
    hist x, discrete width(0.5)
    graph export "`build_analysis'/plot.pdf", replace

    sum x
    file open  outfile using "`build_analysis'/table.txt", write replace
    file write outfile "<tab:table>" _n
    file write outfile (r(mean)) _n (r(sd)) _n (r(max)) _n (r(min))
    file close outfile

    drop x
    set obs 1000000
    egen y = fill(1 3 5 7 9)
    save "`build_analysis'/lg_dataset.dta", replace

end

* EXECUTE
main

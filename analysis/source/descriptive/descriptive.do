version 14
clear all
set more off

program main
    yaml read YAML using constants.yaml
    yaml local data  = YAML.build.prepare_data
    yaml local build = YAML.build.descriptive

    import delimited "`data'/data.txt", delimiter("|") clear
    hist x, discrete width(0.5)
    graph export "`build'/plot.eps", replace

    sum x
    file open  outfile using "`build'/table.txt", write replace
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

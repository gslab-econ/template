version 14
clear all
set more off

program main
    import delimited "output/data/data.txt", delimiters("|") varnames(1) clear
    hist x, discrete width(0.5)
    graph export "output/analysis/plot.eps", replace

    sum x
    file open  outfile using "output/analysis/table.txt", write replace
    file write outfile "<tab:table>" _n
    file write outfile (r(mean)) _n (r(sd)) _n (r(max)) _n (r(min))
    file close outfile
end

* EXECUTE
main

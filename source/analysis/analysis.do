version 14
clear all
set more off


program main
    yaml read YAML using constants.yaml
    yaml local build_data=YAML.build.data
    yaml local build_analysis=YAML.build.analysis

    import delimited "`build_data'/data.txt", delimiters("|") varnames(1) clear
    hist x, discrete width(0.5)
    graph export "`build_analysis'/plot.eps", replace

    sum x
    file open  outfile using "`build_analysis'/table.txt", write replace
    file write outfile "<tab:table>" _n
    file write outfile (r(mean)) _n (r(sd)) _n (r(max)) _n (r(min))
    file close outfile
end


* EXECUTE
main

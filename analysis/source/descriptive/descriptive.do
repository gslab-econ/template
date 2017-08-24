version 14
clear all
set more off

program main
    yaml read YAML using config_global.yaml
    yaml local data  = YAML.build.prepare_data
    yaml local build = YAML.build.descriptive
    import delimited "`data'/data_stata.txt", delimiter("|") clear

    sum x
    file open  outfile using "`build'/table_stata.txt", write replace
    file write outfile "<tab:table>" _n
    file write outfile (r(mean)) _n (r(sd)) _n (r(max)) _n (r(min))
    file close outfile

    hist x, bin(10)
    graph export "`build'/plot_stata.eps", replace
end

* EXECUTE
main

version 14
set more off
preliminaries

program main
    yaml read YAML using config_global.yaml
    yaml global data  = YAML.build.prepare_data
    yaml global build = YAML.build.descriptive

    import delimited "$data/data.txt", delimiter("|") clear

    hist x, bin(10)
    graph export "$build/plot.eps", replace

    tabstat x, stat(mean sd max min) save
    matrix stats = r(StatTotal)
    matrix_to_txt, matrix(stats) saving("$build/table.txt") title("<tab:table>") replace
end

* EXECUTE
main

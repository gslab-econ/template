version 14
set more off
preliminaries

program main
    yaml read YAML using config_global.yaml
    yaml global build = YAML.build.prepare_data

    set obs 300000
    gen x = _n
    export delimited "$build/data.txt", delimiter("|") replace
end

* EXECUTE
main

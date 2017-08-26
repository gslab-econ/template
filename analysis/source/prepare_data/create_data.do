version 14
clear all
set more off

program main
    yaml read YAML using config_global.yaml
    yaml local build = YAML.build.prepare_data

    set obs 300000
    gen x = _n
    export delimited "`build'/data.txt", delimiter("|") replace 
end

* EXECUTE
main

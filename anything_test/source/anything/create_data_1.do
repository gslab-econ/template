version 14
clear all
set more off

program main
    yaml read YAML using config_global.yaml
    yaml local build = YAML.build.prepare_data

    set obs 300000
    egen x = fill(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16)
    export delimited "`build'/data_1.txt", delimiter("|") replace 
end

* EXECUTE
main

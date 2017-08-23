version 14
clear all
set more off

program main
    yaml read YAML using constants.yaml
    yaml local build = YAML.build.prepare_data

    set obs 300000
    egen x = fill(1 2 3 4 5 6 7 8)
    export delimited "`build'/data.txt", delimiter("|") replace 
end

* EXECUTE
main

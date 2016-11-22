version 14
set more off
preliminaries
cap adopath + PERSONAL

program main
    import delimited "build/data/data.txt", delimiters("|") varnames(1) clear
    hist count, discrete width(0.5)
    graph export "output/analysis/plot.eps", replace
    collapse (sum) count, by(group)
    mkmat group count, matrix("result")
    matrix_to_txt, matrix(result) saving("output/analysis/table.txt") title("<tab:table>") replace
end

* EXECUTE
main

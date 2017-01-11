

program main
	syntax, iter(string)
	import delimited "output/data/data_`iter'.txt", delimiter("|") varnames(nonames) clear
	rename v1 obs_value
	gen obs_number = _n
	graph twoway line obs_value obs_number
	graph export "output/analysis/plot.eps"
end

main, iter(`1')

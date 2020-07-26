version 14
set more off
preliminaries

program main
    yaml read YAML using config_global.yaml
    yaml global build = YAML.build.draw_data

    set obs 10000
	matrix mu = (0,0)
	matrix sigma = (1,0 \ 0,1)
	drawnorm x1 x2, means(mu) corr(sigma) cstorage(full) seed(60)
    outsheet using "$build/data.csv", comma replace
end

* EXECUTE
main

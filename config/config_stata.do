clear all
set more off

program main
    * *** Add required packages from SSC to this list ***
    local ssc_packages ""
    * *** Add required packages from SSC to this list ***

    if !missing("`ssc_packages'") {
        foreach pkg in "`ssc_packages'" {
        * install using ssc, but avoid re-installing if already present
            capture which `pkg'
            if _rc == 111 {                 
               dis "Installing `pkg'"
               quietly ssc install `pkg', replace
               }
        }
    }

    * Install packages using net, but avoid re-installing if already present
    capture which yaml
       if _rc == 111 {
        quietly net from "https://raw.githubusercontent.com/gslab-econ/stata-misc/master/"
        quietly cap ado uninstall yaml
        quietly net install yaml
       }
    * Install complicated packages : moremata (which cannot be tested for with which)
    capture confirm file $adobase/plus/m/moremata.hlp
        if _rc != 0 {
        cap ado uninstall moremata
        ssc install moremata
        }
     * Standard GSLAB stuff
    quietly net from "https://raw.githubusercontent.com/gslab-econ/gslab_stata/master/gslab_misc/ado"
       quietly cap net uninstall matrix_to_txt
       quietly net install matrix_to_txt
       quietly cap net uninstall preliminaries
       quietly net install preliminaries

end

main

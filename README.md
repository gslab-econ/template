Using the repository template
=============================

#### Pre-requisites:
 - Mac OS or Linux OS
 - [Python 2.X](https://www.python.org)
    - Executable should be added to the `PATH` environment variable so it is calleble from the command line with `python`
 - [Stata MP](http://www.stata.com/statamp/)
    - Executable should be added to the `PATH` environment variable so it is callable from the command line with `statamp`
 - [R](https://www.r-project.org/)
    - Executable should be added to the `PATH` environment variable so it is callable from the command line with `Rscript`
 - [Lyx](https://www.lyx.org/)
    - Executable should be added to the `PATH` environment variable so it is callable from the command line with `lyx`
 - [scons](http://scons.org/) 2.4.0 or later
    - SCons can also be installed with [pip](https://pip.pypa.io/en/stable/) using `pip install --egg scons`
    - More information about Scons can be found [here](https://github.com/gslab-econ/ra-manual/wiki/SCons)
 - [git-lfs](https://git-lfs.github.com/)
 - [gslab_tools](https://pypi.python.org/pypi/GSLab_Tools) version 1.1.1 or later
    - Installed via `pip install gslab_tools` if [pip](https://pip.pypa.io/en/stable/) is available. 
 - [GSLab-modified Metropolis beamer theme](https://github.com/gslab-econ/gslab_latex)

The easiest way to install all the applications above is to use [Homebrew](http://brew.sh/) on Mac OS and [Linuxbrew](http://linuxbrew.sh/) on Linux, as they will set up the `PATH` variable for you.
E.g., `brew install scons`.

#### To run:
 - The entire directory:
    - In the root directory, type `scons` (or one of its derivatives outlined below). This should run everything that is flagged as being modified or with dependencies that have been modified.
 - A single directory of targets:
    - `scons output/data` will re-build the `output/data` folder if it is out of sync, without rebuilding other files.
 - A single target file:
    - `scons output/paper/paper.pdf` will re-run only the code needed to update `output/paper/paper.pdf` without rebuilding other files.
- Individual scripts can be run directly within Stata and R if they are run in order.

#### Copy the template:
In order to use this repository template for your own purposes, see the [wiki](https://github.com/gslab-econ/template/wiki) for instructions.

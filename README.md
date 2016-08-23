Using the repository template
=============================



#### Pre-requisites:
 - Mac OS or Linux OS
 - [Stata MP](http://www.stata.com/statamp/)
    - Executable should also be added to the `PATH` environment variable so it is callable from the command line with `statamp`
 - [R](https://www.r-project.org/)
    - Executable should also be added to the `PATH` environment variable so it is callable from the command line with `Rscript`
 - [scons](http://scons.org/) 
 - [Lyx](https://www.lyx.org/)
    - Executable should also be added to the `PATH` environment variable so it is callable from the command line with `lyx`
 - [git-lfs](https://git-lfs.github.com/)
 - [GSLab-modified Metropolis beamer theme](https://github.com/gslab-econ/gslab_latex)

 Installing the some of the applications above is easiest with [Homebrew](http://brew.sh/) on Mac OS and [Linuxbrew](http://linuxbrew.sh/) on Linux, as they will set up the PATH variable for you.
 
 E.g., `brew install scons`.
 
 Note: SCons can also be installed with [pip](https://pip.pypa.io/en/stable/) using `pip install --egg scons`.

#### To run:
 - The entire directory:
    - In the root directory, type `scons`. This should run everything that is flagged as being modified or with dependencies that have been modified.
 - A single directory of targets:
    - `scons output/data` will re-build the `output/data` folder if it is out of sync, without rebuilding other files.
 - A single target file:
    - `scons output/paper/paper.pdf` will re-run only the code needed to update `output/paper/paper.pdf` without rebuilding other files.


Individual scripts can be run directly within Stata and R if they are run in order.

#### More information about scons:
  *  [Data analysis with SCons](http://zacharytessler.com/2015/03/05/data-workflows-with-scons/)
  *  [SCons User Guide](http://scons.org/doc/production/PDF/scons-user.pdf)
  *  [SCons Manual](http://scons.org/doc/production/PDF/scons-man.pdf)
  

#### Copy the template:
In order to use this repository template for your own purposes, see the [wiki](https://github.com/gslab-econ/template/wiki) for instructions.

#### License
The MIT License (MIT)
Copyright (c) 2016 Matthew Gentzkow and Jesse M. Shapiro.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


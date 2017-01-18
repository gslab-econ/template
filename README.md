Using the repository template
=============================

#### Pre-requisites:
 - Mac OS or Linux OS
 - [Python 2.X](https://www.python.org)
 - [Stata MP](http://www.stata.com/statamp/)
 - [R](https://www.r-project.org/)
 - [Lyx](https://www.lyx.org/)
    - For the above four, executables need to added to `path` environment variable. So they are callable from the command line with `python`, `statamp`, `Rscript`, and `lyx`.
 - [SCons](http://scons.org/) version 2.4.0 or later
    - SCons can also be installed via [pip](https://pip.pypa.io/en/stable/) using `pip install --egg scons`.
    - More information about Scons can be found [here](https://github.com/gslab-econ/ra-manual/wiki/SCons).
 - [git-lfs](https://git-lfs.github.com/)
 - [gslab_tools](https://pypi.python.org/pypi/GSLab_Tools) version 1.1.1 or later
    - Installed via [pip](https://pip.pypa.io/en/stable/) using `pip install gslab_tools`.
 - [GSLab-modified Metropolis beamer theme](https://github.com/gslab-econ/gslab_latex)

The easiest way to install all the applications above is to use [Homebrew](http://brew.sh/) on Mac OS and [Linuxbrew](http://linuxbrew.sh/) on Linux, as they will set up the `PATH` variable for you, e.g., `brew install scons`.

#### To run:
 - The entire directory:
    - In the root directory, type `scons` in the command line. This should run everything that is flagged as being modified or with dependencies that have been modified.
 - A single directory of targets:
    - `scons output/data` will re-build the `output/data` folder if it is out of sync, without rebuilding other files.
 - A single target file:
    - `scons output/paper/paper.pdf` will re-run only the code needed to update `output/paper/paper.pdf` without rebuilding other files.

#### Copy the template:
In order to create a new repository using this template, either
- Fork this repository
- Create an empty repository in GitHub and clone it locally. Copy the contents of this template into the empty repository. Make sure to exclude the `.git` folder, but include the `.gitattributes` and `.gitignore` files. Re-run the entire directory using `Scons`. Commit and push to the new repository.

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

 Installing the some of the applications above above is easiest with [Homebrew](http://brew.sh/) on Mac OS and [Linuxbrew](http://linuxbrew.sh/) as they will set up the PATH variable for you.
 
 E.g., `brew install scons`.

#### In order to create a new repository using this template:

 - Either:
    - [Fork](https://help.github.com/articles/fork-a-repo/) this repository
    - Create a completely empty repository in GitHub. Clone this empty repository locally. Copy the contents of this template repository into the empty repository (making sure to __exclude__ the `.git` folder, but __include__ the .gitattributes and .gitignore files). Re-run with SCons. Commit and push to the new repository.

#### To run:
 - The entire directory:
    - In the root directory, type 'scons'. This should run everything that is flagged as being modified or with dependencies that have been modified.
 - A single directory of targets:
    - `scons output/data` will re-build the `output/data` folder if it is out of sync, without rebuilding other files.
 - A single target file:
    - `scons output/paper/paper.pdf` will re-run only the code needed to update `output/paper/paper.pdf` without rebuilding other files.


See the following for more information about scons:
  *  [Data analysis with SCons](http://zacharytessler.com/2015/03/05/data-workflows-with-scons/)
  *  [SCons User Guide](http://scons.org/doc/production/PDF/scons-user.pdf)
  *  [SCons Manual](http://scons.org/doc/production/PDF/scons-man.pdf)

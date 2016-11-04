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
  - [gslab_tools](https://pypi.python.org/pypi/GSLab_Tools) version 1.0.7 or later
    - Installed via `pip install gslab_tools` if [pip](https://pip.pypa.io/en/stable/) is available. 
 - [GSLab-modified Metropolis beamer theme](https://github.com/gslab-econ/gslab_latex)
 - Google Drive Desktop App
     - After installing Google Drive, ensure that there is a directory entitled "Google Drive" in the folder whose path is given by entering `echo /Users/$USER` at the command line. Having the Google Drive directory in this location is required for using the remote sync for cache.
 - A GitHub [token](https://help.github.com/articles/creating-an-access-token-for-command-line-use/) is required to create a 'release' per our protocol below.

 Installing the some of the applications above is easiest with [Homebrew](http://brew.sh/) on Mac OS and [Linuxbrew](http://linuxbrew.sh/) on Linux, as they will set up the PATH variable for you.
 
 E.g., `brew install scons`.
 
 Note: SCons can also be installed with [pip](https://pip.pypa.io/en/stable/) using `pip install --egg scons`.

#### To run:
 - The entire directory:
    - In the root directory, type `scons` (or one of its derivatives outlined below). This should run everything that is flagged as being modified or with dependencies that have been modified.
 - A single directory of targets:
    - `scons output/data` will re-build the `output/data` folder if it is out of sync, without rebuilding other files.
 - A single target file:
    - `scons output/paper/paper.pdf` will re-run only the code needed to update `output/paper/paper.pdf` without rebuilding other files.


Individual scripts can be run directly within Stata and R if they are run in order.

#### Cache and release protocol

We observe the following instructions when working with repositories based on the large template (henceforth "large repositories").
- Add the GSLab `cache` and `release` folders from your "Shared with me" folder to your "My Drive" folder on the [Google Drive website](https://www.google.com/drive/). You'll only need to do this once.
- Add directories with the same name as the repository to the the shared GSLab `cache` and `release` folders when beginning a new large repository.  The `release` folder is only necessary if the repository's releases will be stored on Google Drive
- Run scons in *cache* mode after cloning a large repository: `scons mode=cache`.
- Run scons in *develop* mode as you modify code and make intermediate commits to the issue branch: `scons mode=develop`, or just `scons`.
- Run scons in cache mode with [force caching](http://scons.org/doc/2.0.1/HTML/scons-user/x4276.html) before submitting a pull request and merging to master, : `scons mode=cache --cache-force`.
- Create a release by runing scons in *release* mode: `scons mode=release version=issue###`. Note that no code changes should be made at this point - this `scons` run should __only__ push files to Drive or create a tag in GitHub.

#### More information about scons:
  *  [Data analysis with SCons](http://zacharytessler.com/2015/03/05/data-workflows-with-scons/)
  *  [SCons User Guide](http://scons.org/doc/production/PDF/scons-user.pdf)
  *  [SCons Manual](http://scons.org/doc/production/PDF/scons-man.pdf)
  

#### Copy the template:
In order to use this repository template for your own purposes, see the [wiki](https://github.com/gslab-econ/template/wiki) for instructions.

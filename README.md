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
 - Google Drive Desktop App
     - After installing Google Drive, ensure that there is a directory entitled "Google Drive" in your home folder. This is required for using the remote sync for cache.

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


#### "Cache and release" protocol:

- Manually create the relevant 'cache' and 'release' Google Drive folders and share them, assigning ownership as appropriate. If these folders have already created and shared, ensure that you place them within your "My Drive" folder. This all can be done on [Google Drive's website](https://www.google.com/drive/).
	- The 'release' drive folder is only necessary if the releases will be stored on Google Drive instead of GitHub.
- Clone repo
- Run scons in 'cache' mode. `scons mode=cache`.
- Modify code and run scons in 'develop' mode as you make intermediate commits to the issue branch. `scons mode=develop` or just `scons`
- Before submitting a pull request and before merging to master, run scons in 'cache' mode with [force caching](http://scons.org/doc/2.0.1/HTML/scons-user/x4276.html) turned on before committing. `scons mode=cache --cache-force`
- Merge with master
- Create a release by runing scons in 'release' mode (Note that no code changes should be made at this point. This `scons` run should __only__ push files to Drive or create a tag in GitHub). `scons mode=release version=issue###`
- If need to create a release that pushes to google drive, run scons in 'release'+drive mode. `scons drive mode=release version=issue###`

The `release` folder should only store files that will be versioned in GitHub and are intended to be used outside of the directory. `DriveReleaseFiles` should only call files from within `build`, so no extra installation step is necessary.



#### More information about scons:
  *  [Data analysis with SCons](http://zacharytessler.com/2015/03/05/data-workflows-with-scons/)
  *  [SCons User Guide](http://scons.org/doc/production/PDF/scons-user.pdf)
  *  [SCons Manual](http://scons.org/doc/production/PDF/scons-man.pdf)
  

#### Copy the template:
In order to use this repository template for your own purposes, see the [wiki](https://github.com/gslab-econ/template/wiki) for instructions.

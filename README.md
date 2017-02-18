Using the repository template
=============================

#### Pre-requisites:

 - Windows `cmd.exe`, Mac OS X `bash`, or Linux `bash`. 
 - [Python 2.X](https://www.python.org) (add to [PATH](https://en.wikipedia.org/wiki/PATH_(variable)))
 	- Python module: [PyYAML](http://pyyaml.org/wiki/PyYAML)
 - [Stata MP](http://www.stata.com/statamp/) (add to [PATH](https://en.wikipedia.org/wiki/PATH_(variable)))
    - Stata ado file: [yaml](https://github.com/sergiocorreia/stata-misc/tree/75a8b251bec02ba590c862cc395c4b95077d8a95)
 - [R](https://www.r-project.org/) (add to [PATH](https://en.wikipedia.org/wiki/PATH_(variable)))
    - R package: [yaml](https://cran.r-project.org/web/packages/yaml/yaml.pdf)
 - [Lyx](https://www.lyx.org/) (add to [PATH](https://en.wikipedia.org/wiki/PATH_(variable)))
 - [SCons](http://scons.org/) (Note that version 2.4.0 or later is best if using the [cache](http://scons.org/doc/2.0.1/HTML/scons-user/c4213.html)).
    - More information about SCons can be found [here](https://github.com/gslab-econ/ra-manual/wiki/SCons).
 - [git-lfs](https://git-lfs.github.com/)
 - [gslab_tools](https://github.com/gslab-econ/gslab_python) version 4.0.0 or later
 - [GSLab-modified Metropolis beamer theme](https://github.com/gslab-econ/gslab_latex)

The easiest way to install all the applications above is to use [Homebrew](http://brew.sh/) on Mac OS and [Linuxbrew](http://linuxbrew.sh/) on Linux, as they will set up the `PATH` variable for you, e.g., `brew install scons`.

#### To run:
 - The entire directory:
    - In the root directory, type `scons` in the command line. This should run everything that is flagged as being modified or with dependencies that have been modified.
 - A single directory of targets:
    - `scons build/data` will re-build the `build/data` folder if it is out of sync, without rebuilding other files.
 - A single target file:
    - `scons build/paper/paper.pdf` will re-run only the code needed to update `build/paper/paper.pdf` without rebuilding other files.

See [here](https://github.com/gslab-econ/gslab_python/tree/master/gslab_scons) for directions on making a 'release'.

#### Copy the template:
In order to create a new repository using this template, either

- First, either:
	- Fork this repository
	- Create an empty repository in GitHub and clone it locally. Copy the contents of this template into the empty repository. Make sure to exclude the `.git` folder, but include the `.gitattributes` and `.gitignore` files. Re-run the entire directory using `Scons`. Commit and push to the new repository.
- Setup a `user-config.yaml` in the root of the directory with at least the following (note that this file should not be versioned):
```
stata_flavor: statamp
cache: /Users/leviboxell/Google Drive/cache/template

```

#### License

The MIT License (MIT)

Copyright (c) 2016 Matthew Gentzkow, Jesse Shapiro

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

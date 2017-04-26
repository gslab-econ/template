# GSLab Template

The GSLab Template is a minimal working demonstration of the tools and organization used by projects in the GSLab. We use SCons and a few custom builders to execute scripts and track dependencies in a portable and flexible manner.   

## Prerequisites

You'll need the following to run the template. [Homebrew](https://brew.sh/) for Mac and [Linuxbrew](http://linuxbrew.sh/) for Linux make this easier.   
* Windows `cmd.exe`, Mac OS X `bash`, or Linux `bash`. Most users will have these one of these as standard.
* [Python 2.7.X](https://wiki.python.org/moin/BeginnersGuide/Download) for [Windows](https://docs.python.org/2/using/windows.html), [Mac](https://docs.python.org/2/using/mac.html) or [Linux](https://docs.python.org/2/using/unix.html).
    * [gslab_python](https://github.com/gslab-econ/gslab_python) version 4.0.0.
    * [PyYAML](http://pyyaml.org/wiki/PyYAML) a python module for parsing YAML files. 
* [SCons](http://scons.org/pages/download.html) version 2.4 or later.
* [git](https://git-scm.com/downloads) for version control.
    * [git-lfs](https://git-lfs.github.com/) for versioning large files. 
    * You'll need both git and git-lfs to clone the repository. 
* [LyX](https://www.lyx.org/Download) (with instructions for LaTeX) 
    * Add LyX to your PATH for [Windows](http://www.computerhope.com/issues/ch000549.htm), [Mac](http://hathaway.cc/post/69201163472/how-to-edit-your-path-environment-variables-on-mac), and [Linux](http://stackoverflow.com/questions/14637979/how-to-permanently-set-path-on-linux).
* [Stata](http://www.stata.com/)
    * Add Stata to your PATH for [Windows](http://www.computerhope.com/issues/ch000549.htm), [Mac](http://hathaway.cc/post/69201163472/how-to-edit-your-path-environment-variables-on-mac), and [Linux](http://stackoverflow.com/questions/14637979/how-to-permanently-set-path-on-linux).
    * [yaml](https://github.com/gslab-econ/stata-misc) a Stata ado file for parsing YAML files. 

## Getting started

1. Open a shell, clone the repository, and navigate to its root.
    ```
    git clone https://github.com/gslab-econ/template.git
    cd template
    ```
2. You're ready to go. We'll prompt you to enter any information necessary and store it in `user-config.yaml` as your scripts run. 
    * To build everything that has been modified or with dependencies in the repository that have been modified.
        ```
        scons
        ```
    * To build everything in a single directory of targets that has been modified and all of their dependencies that have been modified.
        ```
        scons build/path/to/directory
        ```
    * To build a single target that has been modified and all of its dependencies that have been modified.
        ```
        scons build/path/to/file.ext
        ```

## Copying the template

If you want to create a repository with the same structure as this template you can fork it. If you want a repository without any of our git history, follow these instructions. 
* Create an empty repository in GitHub and clone it. 
* Copy the contents of this template into the empty repository. Make sure to exclude the `.git` folder, but include the `.gitattributes` and `.gitignore` files. 
* Create a `user-config.yaml` file and run `scons`. 
* Commit the changes and push to the new repository.

## FAQ 

##### What is `user-config.yaml`?

Each user is allowed to have different local specifications: We don't put any restrictions on where you keep large files, what you call your executables, or how you manage shared directories. We do need to find these things, and that's what `user-config.yaml` is for. Each user maintains an unversioned [YAML file](http://yaml.org/) with these sorts of specifications. Each script uses its associated yaml-parsing module to read these specifications each time the script is run. 

##### What do I put in `user-config.yaml`?

There's no "default" for `user-config.yaml` because it depends on system specifications and user preferences. Two things we do recommend keeping in `user-config.yaml` are the name of your Stata executable—which we'll prompt you to enter if necessary—and the location of a [SCons cache directory](http://scons.org/doc/2.0.1/HTML/scons-user/c4213.html)—if you have one. An example where Example_User is running a factory-fresh StataMP and has local access to a directory named cache/template on Dropbox would be 
```YAML
stata_exec: statamp # StataMP-64.exe on Windows
cache: /Users/Example_User/Dropbox/cache/template
```

##### Can I only use other software for data analysis?

Yup, we have custom builders for Python and R, and you can use them with the same syntax as the Stata builder. If you're using R, make sure it's been added to your PATH and that you have a YAML-parsing package, such as [yaml](https://cran.r-project.org/web/packages/yaml/yaml.pdf). 

##### Can I write my paper in LaTeX?

We don't have a custom builder for latex. You can still write in it, but you will have to use [SCons's native builder](http://www.scons.org/doc/0.96.91/HTML/scons-user/a5334.html).

##### Can I release to GitHub?

Yes, see [here](https://github.com/gslab-econ/gslab_python/tree/master/gslab_scons) for directions on making a release.

## License

The MIT License (MIT)

Copyright (c) 2017 Matthew Gentzkow, Jesse Shapiro

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

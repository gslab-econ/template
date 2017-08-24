# GSLab Template 

The GSLab Template is a minimal working demonstration of the tools and organization used by projects in the GSLab. We use SCons and a few custom builders to execute scripts and track dependencies in a portable and flexible manner.   

## Prerequisites

You'll need the following to run the template. [Homebrew](https://brew.sh/) for Mac and [Linuxbrew](http://linuxbrew.sh/) for Linux make this easier.   
* Windows `cmd.exe`, Mac OS X `bash`, or Linux `bash`. 
* [Python 2.7.X](https://wiki.python.org/moin/BeginnersGuide/Download) for [Windows](https://docs.python.org/2/using/windows.html), [Mac](https://docs.python.org/2/using/mac.html) or [Linux](https://docs.python.org/2/using/unix.html).
    * [gslab_python](https://github.com/gslab-econ/gslab_python) version 4.1.0 or later.
    * [PyYAML](http://pyyaml.org/wiki/PyYAML) a Python module for parsing YAML files. 
* [SCons](http://scons.org/pages/download.html) version 2.4 or later.
* [git](https://git-scm.com/downloads) for version control.
    * [git-lfs](https://git-lfs.github.com/) for versioning large files. 
    * You'll need both git and git-lfs to clone the repository. 
* [LyX](https://www.lyx.org/Download) (with instructions for LaTeX) 
    * Add LyX to your PATH for [Windows](http://www.computerhope.com/issues/ch000549.htm), [Mac](http://hathaway.cc/post/69201163472/how-to-edit-your-path-environment-variables-on-mac), and [Linux](http://stackoverflow.com/questions/14637979/how-to-permanently-set-path-on-linux).
    * The beamer theme [`metropolis`](https://github.com/matze/mtheme). This is part of MikTeX since Dec 2014. 
* [Stata](http://www.stata.com/)
    * Add Stata to your PATH for [Windows](http://www.computerhope.com/issues/ch000549.htm), [Mac](http://hathaway.cc/post/69201163472/how-to-edit-your-path-environment-variables-on-mac), and [Linux](http://stackoverflow.com/questions/14637979/how-to-permanently-set-path-on-linux).
    * [yaml](https://github.com/gslab-econ/stata-misc) a Stata ado file for parsing YAML files. 

## Getting started

1. Open a shell, clone the repository, and navigate to its root.
    ```
    git clone https://github.com/gslab-econ/template.git
    cd template
    ```
2. You're ready to go. We'll prompt you to enter any necessary information and store it in `config_user.yaml` as your scripts run. 
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
* Copy the contents of this template into the empty repository. Make sure to exclude the `.git` folder, but include the [`.gitattributes`](https://git-scm.com/docs/gitattributes) and [`.gitignore`](https://git-scm.com/docs/gitignore) files. 
* Commit the changes and push to the new repository **(Do not commit `config_user.yaml`)**.

## FAQ 

##### What is `config_user.yaml`?

Each user is allowed to have different local specifications: We don't put any restrictions on where you keep large files, what you call your executables, or how you manage shared directories. We do need to find these things, and that's what `config_user.yaml` is for. Each user maintains an **unversioned** [YAML file](http://yaml.org/) with these sorts of specifications. Each script uses its associated yaml-parsing module to read these specifications each time the script is run. 

##### What do I put in `config_user.yaml`?

There's no "default" for `config_user.yaml` because it depends on system specifications and user preferences. Three things we do recommend keeping in `config_user.yaml` are the name of your Stata executable, the location of a [SCons cache directory](http://scons.org/doc/2.0.1/HTML/scons-user/c4213.html), and the location of a release directory. These fields don't have to be specified if you're not using them, and we'll prompt you for their values at runtime if you've forgotten to specify them and they're necessary. A Mac example where Example_User is running a factory-fresh StataMP and has local access to a directories named cache/template and release on Dropbox would be 

```YAML
stata_executable: stata-mp
cache_directory: /Users/Example_User/Dropbox/cache/template
release_directory: /Users/Example_User/Dropbox/release/
```

##### How do I handle data external to my repository?

We are agnostic about how you incorporate external data into the template. There's no custom builder for these assets, by design. Our suggestions:

* When a large dataset is stored locally, `config_user.yaml` can include an entry specifying the user-specific path to that dataset. The key of the entry should be constant across users and documented in the top-level readme of the repository.

* When a large dataset is stored externally, there are a few options. 
    * The top-level readme can specify manual download and storage instructions. This is simple, easy to customize, and unlikely to cause errors during a SCons build. It does, however, require each user to successfully download the same dataset, perhaps in an unstructured manner. 
    * The download can be incorporated into the SCons build. We either execute a program to transfer data (e.g., `rsync` or `rclone`) directly in a standard SCons command or from within a script executed by one of our custom builders. These methods have the benefits of automation and dependency tracking, but they can introduce idiosyncratic errors if the download steps are prone to failure.
    * Regardless of the download method, the path to the dataset should be added to `config_global.yaml` and `.gitignore` if it is stored within the repository and to `config_user.yaml` if it is stored elsewhere. 

##### Can I use other software for data analysis?

Yes. We have custom builders for Python and R. You can also use them with the same syntax as the Stata builder. If you're using R, make sure it's been added to your PATH and that you have a YAML-parsing package, such as [yaml](https://cran.r-project.org/web/packages/yaml/yaml.pdf). 

##### Can I pass "command line style" arguments to a script?

You bet. All of our custom builders accept "command line style" arguments with the same method. Enumerate the arguments in a list and pass them to the builder through the `CL_ARG` keyword argument, exactly the same way you specify sources and targets. We'll format this list, and `scons` will pass its contents to the script at runtime. You can reference these arguments when writing a script using the standard practice for its language.

##### How is the build process logged?

Each of our custom builders produces a log of its process in the same directory as the first of its targets. Each log is named `sconscript.log` by default, and you can insert custom text between `sconscript` and `.log` by passing it as a string through the builder's `log_ext` keyword argument. It's similar to the way that you specify sources and targets, except that the `log_ext` argument must be a string. You should specify the `log_ext` argument for builders that produce logs in the same directory, otherwise the default `sconscript.log` will be overwritten by each builder.

After all the steps in the build are completed, we'll comb through the directory and look for for any files named `sconscript*.log`. These logs will be concatenated—with the earliest completed ones first and all logs with errors on top. We'll store this concatenated log at the root of the repository in `sconstruct.log`. 

##### Can I write my paper in LaTeX instead of LyX?

We don't have a custom builder for LaTeX. You can still write in it, but you will have to use [SCons's native builder](http://www.scons.org/doc/0.96.91/HTML/scons-user/a5334.html). You can still use our custom table builder to fill LaTeX tables. 

##### Can I release my repository?

Yes, our [custom tool](https://github.com/gslab-econ/gslab_python/tree/master/gslab_scons) allows you to release to GitHub and a local destination specified in `config_user.yaml`. A new release can be transfered to a remote manually (e.g., using `rsync` or `rclone`) or automatically by specifying a local destination that's synced to a remote (e.g., a Dropbox directory). 

Every file intended for release should be added to the `release` directory. Files not intended for release to GitHub should be added to `.gitignore`. Our tool will transfer everything in `release` to the local destination and create a [GitHub release](https://help.github.com/articles/creating-releases/) with all the versioned files—those not added to `.gitignore`—in `release`. 

#### License

The MIT License (MIT)

Copyright (c) 2017 Matthew Gentzkow, Jesse Shapiro

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

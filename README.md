# GSLab Template 

The GSLab Template is a minimal working demonstration of the [tools and organization](https://github.com/gslab-econ/ra-manual/wiki/Getting-Started) used by projects in the GSLab. We use [SCons](http://scons.org/) and a few custom builders to execute scripts and track dependencies in a portable and flexible manner.

## Prerequisites

You'll need the following to run the template. [Homebrew](https://brew.sh/) for Mac and [Linuxbrew](http://linuxbrew.sh/) for Linux make this easier.
* Windows `cmd.exe`, Mac OS X `bash`, or Linux `bash`.
* [Python 2.7.X](https://wiki.python.org/moin/BeginnersGuide/Download) and [pip](https://pip.pypa.io/en/stable/installing/) for [Windows](https://docs.python.org/2/using/windows.html), [Mac](https://docs.python.org/2/using/mac.html) or [Linux](https://docs.python.org/2/using/unix.html).
* [git](https://git-scm.com/downloads) for version control.
    * [git-lfs](https://git-lfs.github.com/) for versioning large files. 
    * You'll need both git and git-lfs to clone the repository. 
* [LyX](https://www.lyx.org/Download) (with instructions for LaTeX) 
    * Add LyX to your PATH for [Windows](http://www.computerhope.com/issues/ch000549.htm), [Mac](http://hathaway.cc/post/69201163472/how-to-edit-your-path-environment-variables-on-mac), and [Linux](http://stackoverflow.com/questions/14637979/how-to-permanently-set-path-on-linux).
    * The beamer theme [`metropolis`](https://github.com/matze/mtheme). This is part of MikTeX since Dec 2014. 

## Quick start

1. Open a shell, clone the repository, and navigate to its root.
    ```bash
    git lfs clone https://github.com/gslab-econ/template.git YourProjectName
    cd YourProjectName
    ```
2. Install Python dependencies ([GSLab Python v4.1.0](https://github.com/gslab-econ/gslab_python/tree/v4.1.0), [PyYAML](http://pyyaml.org/), [numpy](http://www.numpy.org/), and [matplotlib]('matplotlib')).
    ```bash
    # Store package names in this text file.
    pip install -r config/requirements.txt
    ```
3. Unzip the scons package.
    ```bash
    unzip config/scons.zip -d config/scons # Do manually on Windows
    ```
4. Navigate to the `analysis` or `paper_slides` subdirectory.  
    ```bash
    cd analysis
    ```
5. You're ready to go. We'll prompt you to enter any necessary information and store it in `config_user.yaml` as your scripts run. 
    * To build everything in the subdirectory that has been modified or with dependencies in the subdirectory that have been modified.
        ```bash
        python run.py
        ```
    * To build everything in a single directory of targets that has been modified and all of their dependencies that have been modified.
        ```bash
        python run.py build/path/to/directory
        ```
    * To build a single target that has been modified and all of its dependencies that have been modified.
        ```bash
        python run.py build/path/to/file.txt
        ```

## Copying the template

If you want to create a repository with the same structure as this template you can fork it. If you want a repository without any of our git history, follow these instructions. 
* Create an empty repository in GitHub and clone it. 
* Copy the contents of this template into the empty repository. Make sure to exclude the `.git` folder, but include the [`.gitattributes`](https://git-scm.com/docs/gitattributes) and [`.gitignore`](https://git-scm.com/docs/gitignore) files. 
* Commit the changes and push to the new repository **(Do not commit `config_user.yaml`)**.

You can accomplish the last two bullets by running these (Bash) commands. 
```bash
# Get new repository's name
echo "Enter the empty repository's name."     
read REPO_NAME      

# Clone new repository and template
git clone https://github.com/gslab-econ/$REPO_NAME
git lfs clone https://github.com/gslab-econ/template.git

# Copy template's contents to new repository and clean up
rm -rf  template/.git       
cp -a template/ $REPO_NAME/
rm -rf template

# Commit and push new repository   
cd $REPO_NAME
git add .               
git commit -m "Initialized repository with the gslab-econ template."        
git push
```

## FAQ 

#### What is `config_user.yaml`?

Each user is allowed to have different local specifications: We don't put any restrictions on where you keep large files, what you call your executables, or how you manage shared directories. We do need to find these things, and that's what `config_user.yaml` is for. Each user maintains an **unversioned** [YAML file](http://yaml.org/) with these sorts of specifications. Each script uses its associated YAML-parsing module to read these specifications each time the script is run.

If you try to build a directory without `config_user.yaml`, we'll copy a template to your current working directory. You can always switch back to this template by deleting your current `config_user.yaml` and rerunning.

#### What do I put in `config_user.yaml`?

There's no "default" for `config_user.yaml` because it depends on system specifications and user preferences. Three things we do recommend keeping in `config_user.yaml` are the names of your executables, the location of a [SCons cache directory](http://scons.org/doc/2.0.1/HTML/scons-user/c4213.html), and the location of a release directory. These fields don't have to be specified if you're not using them, and we'll prompt you for their values at runtime if you've forgotten to specify them and they're necessary.

#### What is `config_global.yaml`?

The `config_global.yaml` tracks paths, specifications, variables, and software checks that are constant across users. We treat this file in the same manner as `config_user.yaml`, except that we do version `config_global.yaml`.

One important function of `config_global.yaml` is that it tracks the version of [gslab-python](https://github.com/gslab-econ/gslab_python) you expect your users to have installed.

#### How do I handle data external to my repository?

We are agnostic about how you incorporate external data into the template. There's no custom builder for these assets, by design. Our suggestions:

* When a large dataset is stored locally, `config_user.yaml` can include an entry specifying the user-specific path to that dataset. The key of the entry should be constant across users and documented in the top-level readme of the repository.

* When a large dataset is stored externally, there are a few options. 
    * The top-level readme can specify manual download and storage instructions. This is simple, easy to customize, and unlikely to cause errors during a SCons build. It does, however, require each user to successfully download the same dataset, perhaps in an unstructured manner. 
    * The download can be incorporated into the SCons build. We either execute a program to transfer data (e.g., `rsync` or `rclone`) using our "Anything builder" or from within a script executed by one of our other custom builders. These methods have the benefits of automation and dependency tracking, but they can introduce idiosyncratic errors if the download steps are prone to failure.
    * Regardless of the download method, the path to the dataset should be added to `config_global.yaml` and `.gitignore` if it is stored within the repository and to `config_user.yaml` if it is stored elsewhere. 

* Any pointers to directories you store under the `input` key in either configuration yaml file will have their contents checked and recorded at runtime. We complete the check using our `record_dir` function and store its contents in `release/state_of_input.log`.

#### How do I use the outputs of `analysis` as inputs for `paper_slides`?

We recommend that you manually copy the desired files or directories from the `release` directory in `analysis` to a directory called `input` in `paper_slides`. We uncouple these top-level subdirectories to compartmentalize the research process. A busy coauthor can build `paper_slides` in a reproducible manner without wrangling data or repeating a lengthy analysis.  

There are lighter-weight methods to connect these subdirectories, but they may make your project more prone to errors.
* Create a symlink between `analysis/release` and `paper_slides/input` (not platform-independent).
* Point to `analysis/release` from the `config_global.yaml` in `paper_slides` (hard to parse YAML in LyX and LaTeX).

You can recouple the SCons subdirectories by [installing](http://scons.org/doc/1.2.0/HTML/scons-user/c2848.html) the output from `analysis` into `paper_slides` Add the following line to the SConstruct in `analysis`

```  
env.Install('../paper_slides/input', '#release/') 
```

You'll also need to give SCons permission to build targets outside the `analysis` directory; so run

```bash
python run.py ../paper_slides
```

#### What software can I use for data analysis?

We have custom builders for Python, R, Stata, and MATLAB. They all use the same syntax. You'll need to add the builder to the SCons environment by uncommenting its definition in the SConstruct. Also check that its executable has been added to your PATH and recorded in `config_user.yaml`.

See `analysis/source/prepare_data/` for sample scripts in each language. To run one of the sample scripts, uncomment its block in `analysis/source/prepare_data/SConscript` and its builder in `analysis/SConstruct`. Note that all sample scripts produce the same output, so only one block is allowed to run for each SCons build. If you uncomment the block for one software, you need to comment out the blocks for all others.

* If you're using R, make sure you've installed its dependencies. 
```bash
Rscript config/config_r.r
```
* If you're using Stata, make sure the executable is stored in `config_user.yaml` with the key `stata_executable` and that you've installed its dependencies.
```
statamp -e config/config_stata.do // Stata executable may be different
```
* If you're using Matlab, make sure it's been added to your PATH and that you have installed the Matlab YAML parser following the instructions [here](https://github.com/gslab-econ/gslab_matlab/blob/f11eff492e0c982cf344c60b7e7ce0e7b7a66872/README.md#installation-instructions-for-matlab-r2016b).

#### Can I write my paper in LaTeX instead of LyX?

Yes. We also have the LaTeX builder. See `paper_slides/source/paper` for a demonstration.

#### Is there support for other software?

We support additional software through our "Anything builder." It let's you execute shell commands as a build step using the syntax, logging, and error management of our other custom builders. We turn your commands into a SCons node at runtime, and SCons will track your dependencies and build the node if necessary. SCons will always execute your commands using your system's shell, and you can use this functionality to incorporate arbitrary steps into your build.

An example using standard Bash commands is in `analysis/source/prepare_data/SConscript` and `analysis/source/prepare_data/build_data.sh`. This code won't run on Windows.

#### Can I pass "command line style" arguments to a script?

You bet. All of our custom builders accept "command line style" arguments with the same method. Enumerate the arguments in a list and pass them to the builder through the `CL_ARG` keyword argument, exactly the same way you specify sources and targets. We'll format this list, and `scons` will pass its contents to the script at runtime. You can reference these arguments when writing a script using the standard practice for its language.

#### How is the build process logged?

Each of our custom builders produces a log of its process in the same directory as the first of its targets. Each log is named `sconscript.log` by default, and you can insert custom text between `sconscript` and `.log` by passing it as a string through the builder's `log_ext` keyword argument. It's similar to the way that you specify sources and targets, except that the `log_ext` argument must be a string. You should specify the `log_ext` argument for builders that produce logs in the same directory, otherwise the default `sconscript.log` will be overwritten by each builder.

After all the steps in the build are completed, we'll comb through the directory and look for for any files named `sconscript*.log`. These logs will be concatenated—with the earliest completed ones first and all logs with errors on top. We'll store this concatenated log in `release/sconstruct.log`. 

#### Can I release my repository?

Yes, our [custom tool](https://github.com/gslab-econ/gslab_python/tree/master/gslab_scons) allows you to release to GitHub and a local destination specified in `config_user.yaml`. A new release can be transfered to a remote manually (e.g., using `rsync` or `rclone`) or automatically by specifying a local destination that's synced to a remote (e.g., a Dropbox directory). 

Every file intended for release should be added to the `release` directory. Files not intended for release to GitHub should be added to `.gitignore`. Our tool will transfer everything in `release` to the local destination and create a [GitHub release](https://help.github.com/articles/creating-releases/) with all the versioned files—those not added to `.gitignore`—in `release`.

Our custom tool creates a local release of the SCons subdirectory in which its run but a GitHub release of the entire repository. We therefore suggest you prepend the name of the SCons subdirectory to the title of the release.

#### What if there are large files I need to put in `release` that cannot be versioned?

Our protocol is to keep these files in a designated subdirectory named `release/lg`. By default, `release/lg` is in `.gitignore`. When you use our custom release tool, `release/lg` will be included in the local destination release but not pushed to GitHub.

#### Can I use my system-wide SCons installation?

That's fine, but you'll need version 2.4.0 or later. Just switch `python run.py` to `scons`. Everything else stays the same. You can also skip the unzip step of the Quick Start.

Be aware that the [formatting of the cache](https://bitbucket.org/scons/scons/src/rel_2.5.1/src/CHANGES.txt?at=2.5.1&fileviewer=file-view-default#CHANGES.txt-60) changed in version 2.5.0 of SCons. A cache can get messy and fall out of sync if collaborators use a mix of older and newer versions. 

The version of SCons packaged with this repository is scons-local-3.0.1. Our `run.py` scripts are just wrappers around the `scons.py` included in scons-local. These files exist only to execute SCons, and you shouldn't need to edit them frequently, if at all. The structure of your SCons tree should be entirely specified in your SConstruct and SConscript files.

#### Where should I track the prerequisites for my repository?

Required packages for Python, R, and Stata should be added to their configuration scripts under `config`. If you require the installation of many packages for another language, we suggest you set up a new configuration script in the same location. Other requirements can be added a la carte to the Prerequisites section of this readme. 

#### I use Sublime Text. Is there a custom theme for GSLab-produced logs? 

See [here](https://github.com/gslab-econ/template/wiki/Sublime-Text-syntax-highlighting).

## License

The MIT License (MIT)

Copyright (c) 2017 Matthew Gentzkow, Jesse Shapiro

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

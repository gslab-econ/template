Notes on release.py
-------------------

Make a release from an SCons directory by running the following
from the command line within the directory of interest:
    ```
    python -m gslab_scons.release version=<version name here>
    ```
where `<version name here>` is the name of the version that
the user wishes to release. As an example, to release version
v1.2.1 of a directory, one would run:
    ```
    python -m gslab_scons.release version=v1.2.1
    ```
from the root of the directory. 
Including the option `no_zip` will prevent the release files
from being zipped before their release to Google Drive.

This release procedure will warn the user when a versioned file
is larger than 2MB and when the directory's versioned content
is larger than 500MB in total.  

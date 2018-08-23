#!bin/bash
# Confirm that the user wishes to conduct the build
echo "Before running this script, ensure that:"
echo "- The system requirements of Homebrew are satisfied"
echo "- Xcode, Git, and Python 2 have been set up for command-line use on your machine"
echo "- You have set up your computer to retrieve files from GitHub using the SSH protocol."
echo    "WARNING 1: this script uses sudo and may affect files in your base directories."
read -p "WARNING 2: This script may overwrite or duplicate existing programs and/or default executables. Would you like to continue? [y/n]? " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    # Install Homebrew
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    
    # Basic system applications
    brew install wget
    brew install gdrive
    brew install git-lfs
    brew install scons
    
    # Graphical applications
    sudo xcodebuild -license
    brew cask install cyberduck
    brew cask install dashlane
    brew cask install dropbox
    brew cask install evernote
    brew cask install github-desktop
    brew cask install google-chrome
    brew cask install google-drive

    brew cask install r
    brew cask install rstudio
    brew cask install skype
    
    # LaTeX/LyX set-up
    brew cask install mactex
    brew cask install lyx
    
    git clone git@github.com:gslab-econ/mtheme
    sudo mkdir -p /usr/local/texlive/texmf-local/tex/latex/beamer/themes/gslab
    rm -f /usr/local/texlive/texmf-local/tex/latex/beamer/themes/gslab/*.sty
    sudo mv mtheme/*_gslab.sty /usr/local/texlive/texmf-local/tex/latex/beamer/themes/gslab
    rm -rf mtheme
    sudo texhash
    
    # Python module installation
    sudo easy_install pip
    sudo pip install --upgrade pip
    sudo pip install numpy
    sudo pip install pandas
    sudo pip install scipy
    sudo pip install requests
    pip install git+ssh://git@github.com/gslab-econ/gslab_python.git  
      
    # R package installation
    curl -o Rpackage_build.R 'https://raw.githubusercontent.com/gslab-econ/gslab_r/master/Rpackage_build.R'
    Rscript Rpackage_build.R
    rm Rpackage_build.R 

    # Stata package installation
    # from gslab-econ/gslab_stata
    cd /Users/$USER/
    statamp -e sysdir
    STATA_PERSONAL_DIR=$(cat stata.log | grep 'PERSONAL' | sed 's/PERSONAL:  ~//')
    STATA_PERSONAL_DIR=/Users/$USER$STATA_PERSONAL_DIR
    rm stata.log
    git clone git@github.com:gslab-econ/gslab_stata.git
    cd gslab_stata
    mkdir -p "$STATA_PERSONAL_DIR"
    # http://unix.stackexchange.com/questions/67503/move-all-files-with-a-certain-extension-from-multiple-subdirectories-into-one-di
    find ./ -name  "*.ado" -exec cp "{}" "$STATA_PERSONAL_DIR" \;
    find ./ -name  "*.hlp" -exec cp "{}" "$STATA_PERSONAL_DIR" \;
    cd ..
    rm -rf gslab_stata
    # from forked yaml parser in gslab-econ/stata-misc
    statamp -e "cap net uninstall yaml"
    statamp -e "net install yaml, from(https://raw.githubusercontent.com/gslab-econ/stata-misc/master/)"
    rm stata.log

    # Rclone installation
    cd && curl -O https://downloads.rclone.org/rclone-current-osx-amd64.zip
    unzip -a rclone-current-osx-amd64.zip && cd rclone-*-osx-amd64
    sudo mv rclone /usr/local/bin/
    cd .. && rm -rf rclone-*-osx-amd64 rclone-current-osx-amd64.zip
fi

clear

export BASH_CONF="bash_profile"
[[ -s ~/.bashrc ]] && source ~/.bashrc

#   Set Paths
#   (Check that these match locations of appropriate binaries)
#   ------------------------------------------------------------
export PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin
export PATH="$PATH:/sbin:/opt/X11/bin:/Library/TeX/texbin"
export PATH="$PATH:/usr/local/texlive/2016/bin/universal-darwin"
export PATH="$PATH:/Applications/Lyx.app/Contents/MacOS"
export PATH="$PATH:/~/knitro"
export PATH="$PATH:~/bin"
export PATH="$PATH:/Applications/Stata/StataMP.app/Contents/MacOS"
export PATH="$PATH:/Applications/Stata/StataSE.app/Contents/MacOS"
export PATH="$PATH:/Applications/R.app/Contents/MacOS"
export PATH="$PATH:/Applications/Lyx.app/Contents/MacOS"
export PATH="$PATH:/Applications/Sublime Text.app/Contents/MacOS"
export PATH="$PATH:/Applications/Postgres.app/Contents/Versions/9.4/bin"
export PATH="$PATH:/Applications/MATLAB_R2016b.app/bin"
export PATH="$PATH:/Applications/knitro-10.1.1-z-MacOSX-64/knitroampl"

#   Set PATH for Python 2.7
#   The orginal version is saved in .bash_profile.pysave
export PATH="/Library/Frameworks/Python.framework/Versions/2.7/bin:${PATH}"

#   Set Environment Variables
#   -------------------------------
export gslab_make_path="https://econ-gentzkow-svn.stanford.edu/repos/main/trunk/lib/python/gslab_make/"

#   Set Aliases & Tools
#   -------------------------------
alias cp='cp -iv'                           # Preferred 'cp' implementation
alias mv='mv -iv'                           # Preferred 'mv' implementation
alias mkdir='mkdir -pv'                     # Preferred 'mkdir' implementation
alias ll='ls -FGlhp'                        # Preferred 'ls' implementation
alias less='less -FSRXc'                    # Preferred 'less' implementation
alias edit='subl'                           # edit:         Opens any file in sublime editor
alias f='open -a Finder ./'                 # f:            Opens current directory in MacOS Finder
alias c='clear'                             # c:            Clear terminal display
trash () { command mv "$@" ~/.Trash ; }     # trash:        Moves a file to the MacOS trash
ql () { qlmanage -p "$*" >& /dev/null; }    # ql:           Opens any file in MacOS Quicklook Preview
alias DT='tee ~/Desktop/terminalOut.txt'    # DT:           Pipe content to file on MacOS Desktop
git config --global alias.co checkout
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.br branch

spotlight () { mdfind "kMDItemDisplayName == '$@'wc"; }

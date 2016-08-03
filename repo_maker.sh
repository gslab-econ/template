#!/usr/bin/env bash
# Run this script from the /template/ directory.
echo "Enter the new gslab-econ repository's name here."
read REPO_NAME

cd ..

git clone git@github.com:gslab-econ/$REPO_NAME

# Remove the template's .git repository
rm -rf  template/.git

cp -a template/ $REPO_NAME/

rm -rf template

cd $REPO_NAME

rm repo_maker.sh

git add .gitignore
git add .


git commit -m "Initialised repository with the gslab-econ template."
git push

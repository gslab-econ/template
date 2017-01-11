import requests
import getpass
import re
import json
import time
import os
import sys
import shutil
import subprocess

from _exception_classes import ReleaseError


def release(vers, org, repo, 
            DriveReleaseFiles = [],  
            local_release     = '',  
            target_commitish  = '', 
            zip_release       = True):
    '''Publish a release

    Parameters
    ----------
    env: an SCons environment object
    vers: the version of the release
    DriveReleaseFiles a optional list of files to be included in a
        release to Google Drive.
    local_release: The path of the release directory on the user's computer.
    org: The GtHub organisaton hosting the repository specified by `repo`.
    repo: The name of the GitHub repository from which the user is making
        the release.
    '''
    # Check the argument types


    token         = getpass.getpass("Enter a GitHub token and then press enter: ") 
    tag_name      = vers
    releases_path = 'https://%s:@api.github.com/repos/%s/%s/releases' \
                    % (token, org, repo)
    session       = requests.session()

    # Create release
    payload = {'tag_name':         tag_name, 
               'target_commitish': target_commitish, 
               'name':             tag_name, 
               'body':             '', 
               'draft':            'FALSE', 
               'prerelease':       'FALSE'}

    json_dump = json.dumps(payload)
    json_dump = re.sub('"FALSE"', 'false', json_dump)
    posting = session.post(releases_path, data = json_dump)
    # Check that the GitHub release was successful
    posting.raise_for_status()

    # Release to Google Drive
    if bool(DriveReleaseFiles):
        # Delay
        time.sleep(1)
    
        if isinstance(DriveReleaseFiles, basestring):
            DriveReleaseFiles = [DriveReleaseFiles]

        # Get release ID
        json_releases  = session.get(releases_path)
        # Check that the request was successful
        json_releases.raise_for_status()

        json_output    = json_releases.content
        json_split     = json_output.split(',')
        # The id for each tag appears immediately before its tag name
        # in the releases json object.
        tag_name_index = json_split.index('"tag_name":"%s"' % tag_name)
        release_id     = json_split[tag_name_index - 1].split(':')[1]
    
        # Get root directory name on Drive
        path     = local_release.split('/')
        layers   = len(path)
        dir_name = None

        for i in range(layers):
            if path[i] == 'release' and i + 1 < layers:
                dir_name = path[i + 1]
                break

        if dir_name is None:
            raise ReleaseError("No /release/ superdirectory found in path given by local_release")

        if not os.path.isdir(local_release):
            os.makedirs(local_release)
       
        # If the files released to Google Drive are to be zipped,
        # specify their copy destination as an intermediate directory
        if zip_release:
            archive_files = 'release_content'
            if os.path.isdir(archive_files):
                shutil.rmtree(archive_files)
            os.makedirs(archive_files)

            destination_base = archive_files
            drive_header = 'Google Drive: release/%s/%s/release_content.zip' % \
                            (dir_name, vers)
        # Otherwise, send the release files directly to the local release
        # Google Drive directory
        else:
            destination_base = local_release
            drive_header = 'Google Drive:'

        for path in DriveReleaseFiles:
            file_name   = os.path.basename(path)
            folder_name = os.path.dirname(path)
            destination = os.path.join(destination_base, folder_name)
            if not os.path.isdir(destination):
                os.makedirs(destination)
            shutil.copy(path, os.path.join(destination, file_name))
        
        if zip_release:
            shutil.make_archive(archive_files, 'zip', archive_files)
            shutil.rmtree(archive_files)
            shutil.move(archive_files + '.zip', os.path.join(local_release, 'release.zip'))

        if not zip_release:
            DriveReleaseFiles = map(lambda s: 'release/%s/%s/%s' % (dir_name, vers, s), 
                                    DriveReleaseFiles)

        with open('gdrive_assets.txt', 'wb') as f:
            f.write('\n'.join([drive_header] + DriveReleaseFiles))

        upload_asset(token      = token, 
                     org        = org, 
                     repo       = repo, 
                     release_id = release_id, 
                     file_name  = 'gdrive_assets.txt')

        os.remove('gdrive_assets.txt')


def upload_asset(token, org, repo, release_id, file_name, 
                 content_type = 'text/markdown'):
    '''
    This function uploads a release asset to GitHub.

    --Parameters--
    token: a GitHub token
    org: the GitHub organisation to which the repository associated
        with the release belongs
    repo: the GitHub repository associated with the release
    release_id: the release's ID
    file_name: the name of the asset being released
    content_type: the content type of the asset. This must be one of
        types accepted by GitHub. 
    '''
    session = requests.session()

    if not os.path.isfile(file_name):
        raise ReleaseError('upload_asset() cannot find file_name')

    files  = {'file' : open(file_name, 'rU')}
    header = {'Authorization': 'token %s' % token, 
              'Content-Type':  content_type}
    upload_path = 'https://uploads.github.com/repos/%s/%s/releases/%s/assets?name=%s' % \
                  (org, repo, release_id, file_name)
 
    r = session.post(upload_path, files = files, headers = header)
    return r.content


def up_to_date(mode = 'scons', directory = '.'):
    '''
    If mode = scons, this function checks whether the targets of a 
    directory run using SCons are up to date. 
    If mode = git, it checks whether the directory's sconsign.dblite has
    changed since the latest commit.
    '''
    original_directory = os.getcwd()
    os.chdir(directory)

    if mode == 'scons':
        # If mode = scons, conduct a dry run to check whether 
        # all targets are up-to-date
        command = 'scons ' + directory + ' --dry-run'
    elif mode == 'git':
        # If mode = git, check whether .sconsign.dblite has changed
        # since the last commit.
        original_directory = os.getcwd()
        os.chdir(directory)
        command = 'git status'
    
    logpath = '.temp_log_up_to_date'
    
    with open(logpath, 'wb') as temp_log:
        subprocess.call(command, stdout = temp_log, stderr = temp_log, shell = True)
    with open(logpath, 'rU') as temp_log:
        output = temp_log.readlines()
    os.remove(logpath)
    
    # Strip the output lines of white spaces.
    output = map(lambda s: s.strip(), output)

    if mode == 'scons':
        # First, determine whether the directory specified as a function
        # argument is actually a SCons directory.
        # We use the fact that running scons outside of SCons directory
        # produces the message: "No SConstruct file found."
        if [True for out in output if re.search('No SConstruct file found', out)]:
            raise ReleaseError('up_to_date(mode = scons) must be run on a '
                               'SCons directory.')
        # If mode = scons, look for a line stating that the directory is up to date.
        result = [True for out in output if re.search('is up to date\.$', out)]

    elif mode == 'git':  
        # Determine whether the directory specified as a function
        # argument is actually a git repository.
        # We use the fact that running `git status` outside of a git directory
        # produces the message: "fatal: Not a git repository"
        if [True for out in output if re.search('Not a git repository', out)]:
            raise ReleaseError('up_to_date(mode = git) must be run on a '
                               'git repository.')

        # If mode = git, look for a line stating that sconsign.dblite has changed
        # since the latest commit.
        result = [out for out in output if re.search('sconsign\.dblite', out)]
        result = [True for out in result if re.search('modified', out)]
        result = not bool(result)

    os.chdir(original_directory)

    # Return the result.
    return bool(result)


def extract_dot_git(path = '.git'):
    '''
    Extract information from a GitHub repository from a
    .git directory

    This functions returns the repository, organisation, and 
    branch name of a cloned GitHub repository. The user may
    specify an alternative path to the .git directory through
    the optional `path` argument.
    '''
    # Read the config file in the repository's .git directory
    try:
        with open('%s/config' % path, 'rU') as config:
            details = config.readlines()
    except:
        raise ReleaseError("Could not read " + path + "/config. It may not exist")

    # Clean each line of this file's contents
    details = map(lambda s: s.strip(), details)
    
    # Search for the line specifying information for origin
    origin_line = [bool(re.search('\[remote "origin"\]', detail)) \
                   for detail in details]
    origin_line = origin_line.index(True)
    
    # The next line should contain the url for origin
    incr = 1
    url_line  = details[origin_line + incr]
    # If not, keep looking for the url line
    while not re.search('^url =', url_line) and origin_line + incr + 1 <= len(details):
        incr += 1
        url_line  = details[origin_line + increment]
    
    # Extract information from the url line
    # We expect one of:
    # SSH: "url = git@github.com:<organisation>/<repository>/.git"
    # HTTPS: "https://github.com/<organisation>/<repository>.git"
    repo_info   = re.findall('github.com[:/]([\w-]+)/([\w-]+)', url_line)
    organisation = repo_info[0][0]
    repo         = repo_info[0][1]

    # Next, find the branch's name
    with open('%s/HEAD' % path, 'rU') as head:
        branch_info = head.readlines()
    branch = re.findall('ref: refs/heads/([\w-]+)', branch_info[0])[0]

    return repo, organisation, branch


def create_size_dictionary(path):
    '''
    This function creates a dictionary reporting the sizes of
    files in the directory specified by `path`, a string. 
    The filenames are the dictionary's keys; their sizes in 
    bytes are its values. 
    '''
    size_dictionary = dict()

    if not os.path.isdir(path):
        raise ReleaseError("The path argument does not specify an existing directory.")

    for root, directories, files in os.walk(path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            size      =  os.path.getsize(file_path)
            size_dictionary[file_path] = size

    return size_dictionary

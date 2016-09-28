import os, sys, shutil, subprocess, requests, json, re, getpass, time
from sys import platform
from gslab_fill.tablefill import tablefill

def start_log(mode, vers, log = "sconstruct.log"):
  # Prints to log file and shell for *nix platforms
  unix = ["darwin", "linux", "linux2"]
  if platform in unix: 
    sys.stdout = os.popen("tee %s" % log, "w")

  # Prints to log file only for Windows.  
  if platform == "win32":
    sys.stdout = open(log, "w")

  sys.stderr = sys.stdout 
  if not (mode in ['develop', 'cache', 'release']):
     print("Error: %s is not a defined mode" % mode)
     sys.exit()

  if mode == 'release' and vers == '':
      print("Error: Version must be defined in release mode")
      sys.exit()

  return None

def Release(env, vers, DriveReleaseFiles = '', local_release = '', org = 'gslab-econ', \
            repo = 'template', target_commitish = 'master'):
    token         = getpass.getpass("Enter github token and then press enter: ") 
    tag_name      = vers
    releases_path = 'https://%s:@api.github.com/repos/%s/%s/releases' % (token, org, repo)
    session       = requests.session()

    ## Create release
    payload = {'tag_name':tag_name, 'target_commitish':target_commitish, \
        'name':tag_name, 'body':'', 'draft':'FALSE', 'prerelease':'FALSE'}
    json_dump = json.dumps(payload)
    json_dump = re.sub('"FALSE"', 'false', json_dump)
    session.post(releases_path, data = json_dump)

    ## Delay
    time.sleep(1)

    ## Get release ID
    json_releases  = session.get(releases_path)
    json_output    = json_releases.content
    json_split     = json_output.split(',')
    tag_name_index = json_split.index('"tag_name":"%s"' % tag_name)
    release_id     = json_split[tag_name_index - 1].split(':')[1]
    
    ## Release Drive
    if DriveReleaseFiles != '':
        env.Install(local_release, DriveReleaseFiles)
        env.Alias('drive', local_release)
        DrivePath = DriveReleaseFiles
        for i in range(len(DrivePath)):
            path         = DrivePath[i]
            path         = path.split('/')
            DrivePath[i] = 'release/%s/%s/%s' % (repo, vers, path[len(path) - 1])
        with open('gdrive_assets.txt', 'w') as f:
            f.write('\n'.join(['Google Drive:'] + DrivePath))
        uploadAsset(token, org, repo, release_id, 'gdrive_assets.txt')
        os.system('rm gdrive_assets.txt')

def uploadAsset(token, org, repo, release_id, file_name, content_type = 'text/markdown'):
    session = requests.session()
    files = {'file' : open(file_name, 'rb')}
    header = {'Authorization':'token %s' % token, 'Content-Type': content_type}
    upload_path = 'https://uploads.github.com/repos/%s/%s/releases/%s/assets?name=%s' % \
                (org, repo, release_id, file_name)

    r = session.post(upload_path, files = files, headers = header)
    return r.content

def build_tables(target, source, env):
    tablefill(input    = ' '.join(env.GetBuildPath(env['INPUTS'])), 
              template = env.GetBuildPath(source[0]), 
              output   = env.GetBuildPath(target[0]))
    return None

def build_lyx(target, source, env):
    source_file = str(source[0])
    target_file = str(target[0])
    target_dir  = os.path.dirname(target_file)
    newpdf      = source_file.replace('.lyx','.pdf')
    log_file    = target_dir + '/sconscript.log'
    os.system('lyx -e pdf2 %s >> %s' % (source_file, log_file))
    shutil.move(newpdf, target_file)
    return None

def build_r(target, source, env):
    source_file = str(source[0])
    target_file = str(target[0])
    target_dir  = os.path.dirname(target_file)
    log_file    = target_dir + '/sconscript.log'
    os.system('Rscript %s >> %s' % (source_file, log_file))
    return None

def build_stata(target, source, env, executable = 'StataMP'):
    source_file = str(source[0])
    target_file = str(target[0])
    target_dir  = os.path.dirname(target_file)
  
    if platform == "darwin":
      log_file  = target_dir + '/sconscript.log'
      loc_log   = os.path.basename(source_file).replace('.do','.log')
      if executable == 'StataSE':
        os.system('statase -e %s ' % source_file)        
      elif executable == 'Stata':
        os.system('stata -e %s ' % source_file)
      elif executable == 'StataMP': 
        try:
          subprocess.check_output('statamp -e ' + source_file, shell=True)
        except subprocess.CalledProcessError:       
          try: 
            subprocess.check_output('statase -e ' + source_file, shell=True)      
          except subprocess.CalledProcessError:     
            subprocess.check_output('stata -e ' + source_file, shell=True)      
      shutil.move(loc_log, log_file)

    if platform == "linux" or platform == "linux2":
      log_file  = target_dir + '/sconscript.log'
      loc_log   = os.path.basename(source_file).replace('.do','.log')
      if executable == 'StataSE':
        os.system('statase -b %s ' % source_file)        
      elif executable == 'Stata':
        os.system('stata -b %s ' % source_file)
      elif executable == 'StataMP': 
        try:
          subprocess.check_output('statamp -b ' + source_file, shell=True)
        except subprocess.CalledProcessError:       
          try: 
            subprocess.check_output('statase -b ' + source_file, shell=True)      
          except subprocess.CalledProcessError:     
            subprocess.check_output('stata -b ' + source_file, shell=True)      
      shutil.move(loc_log, log_file)

    return None

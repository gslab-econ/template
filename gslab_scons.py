import os, sys, shutil, subprocess, re
from sys import platform
from gslab_fill.tablefill import tablefill

def start_log(log = "sconstruct.log"):
  check_lfs()
  
  # Prints to log file and shell for *nix platforms
  unix = ["darwin", "linux", "linux2"]
  if platform in unix: 
    sys.stdout = os.popen("tee %s" % log, "w")

  # Prints to log file only for Windows.  
  if platform == "win32":
    sys.stdout = open(log, "w")

  sys.stderr = sys.stdout 
  return None

def check_lfs():
    try:
        output = subprocess.check_output("git-lfs install", shell = True)
    except:
        try:
            output = subprocess.check_output("git-lfs init", shell = True) # init is deprecated version of install
        except:
            sys.exit('''ERROR: Either Git LFS is not installed or your Git LFS settings need to be updated. 
                  Please install Git LFS or run 'git lfs install --force' if prompted above.''')

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

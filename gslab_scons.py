import os, sys, shutil, subprocess
from sys import platform
from gslab_fill.tablefill import tablefill

def start_log(log = "sconstruct.log"):
  unix = ["darwin", "linux", "linux2"]
  
  if platform in unix: 
    sys.stdout = os.popen("tee %s" % log, "w")
  elif platform == "win32":
    sys.stdout = open(log, "w")

  sys.stderr = sys.stdout 
  return None

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

def build_stata(target, source, env):
    source_file  = str(source[0])
    target_file  = str(target[0])
    target_dir   = os.path.dirname(target_file)
    executable   = env["stata_flavour"]
  
    unix         = ["darwin", "linux", "linux2"]
    unix_options = ["-e"    , "-b"   , "-b"    ]
    
    # List of executables to be tried
    exec_list    = ["statamp", "statase", "stata"]
    if executable in exec_list:
        exec_list  = [executable]

    if platform in unix:
        log_file = target_dir + '/sconscript.log'
        loc_log  = os.path.basename(source_file).replace('.do','.log')

        # Picking out appropriate option based on platform
        option   = dict(zip(unix, unix_options))[platform]

        for x in exec_list:
            command  = x + " " + option + " %s "
            try: 
                # Call `x' flavour of Stata here
                subprocess.check_output(command % source_file, shell = True)
                break
            except subprocess.CalledProcessError:
                continue

    shutil.move(loc_log, log_file)
    return None

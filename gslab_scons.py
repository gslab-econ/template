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
    unix         = ["darwin", "linux", "linux2"]

    # List of flavors to be tried, dependent on input
    user_flavor  = env["user_flavor"]  
    flavors      = ["StataMP", "StataSE", "Stata"]
    if user_flavor != None:
        flavors  = [user_flavor]

    log_file = target_dir + '/sconscript.log'
    loc_log  = os.path.basename(source_file).replace('.do','.log')
    
    for flavor in flavors:
        try: 
            if platform in unix:
                command = stata_command_unix(flavor)
            elif platform == "win32":
                command = stata_command_win(flavor)
            subprocess.check_output(command % source_file, shell = True)
            break
        except subprocess.CalledProcessError:
            continue

    shutil.move(loc_log, log_file)
    return None

def stata_command_unix(flavor):
    options  = {"darwin": "-e",
                "linux" : "-b",
                "linux2": "-b"}
    option   = options[platform]
    command  = str.lower(flavor) + " " + option + " %s "
    return command

def stata_command_win(flavor):
    if Is64Windows():
        flavor = flavor + "-64"
    command  = flavor + ".exe " + "/e" + " %s "
    return command


def Is64Windows():
    return 'PROGRAMFILES(X86)' in os.environ
    
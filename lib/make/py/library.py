# GIT make.py library
import os, shutil, datetime, subprocess, sys

def check_lfs():
    try:
        output = subprocess.check_output("git lfs init", shell = True)
    except:
        sys.exit("ERROR: Git LFS is not installed. Please install.")
    
# Checks LFS upon loading library
check_lfs()

def clear_dir(dir, path = False):
    if path == True:
        dir = os.environ[dir]
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)

def set_envir_var(name, string):
    os.environ[name] = string
    return os.environ[name]

def load_paths(paths_file_var, paths_file):
    set_envir_var(paths_file_var, paths_file)
    with open(paths_file) as f:
        content = f.readlines()
    for line in content:
        name = line.split("\t")[0]
        value = line.split("\t")[1].split("\n")[0]
        set_envir_var(name, value)

def run_R(program, make_log, local = True, nodes = "1", jobname = "", time = "2:0:0", memPerCPU = "2000"):
    program = set_envir_var("PROGRAM", program)
    make_log = set_envir_var("MAKELOG", make_log)
    if local == True:
        log = open(make_log, "a")
        log.write("Starting " + program + " at " + datetime.datetime.now().strftime("%m/%d/%y:%H:%M:%S") + "\n")
        log.close()
        os.system("Rscript " + program + " >> " + make_log + " 2>&1")
        log = open(make_log, "a")
        log.write("Finished " + program + " at " + datetime.datetime.now().strftime("%m/%d/%y:%H:%M:%S") + "\n")
        log.close()
    if local == False:
        os.system("sbatch -N" + nodes + " -J" + jobname + " --time=" + time + " --mem-per-cpu=" + memPerCPU + " lib/make/sbatch/runR.sbatch") 
 
def run_StataMP(program, make_log):
    program = set_envir_var("PROGRAM", program)
    make_log = set_envir_var("MAKELOG", make_log) 
    log = open(make_log, "a")
    log.write("Starting " + program + " at " + datetime.datetime.now().strftime("%m/%d/%y:%H:%M:%S") + "\n")
    log.close()

    os.system("statamp -e do " + program + " >> " + make_log + " 2>&1")
    stata_logname = program.split('/')[-1]
    stata_logname = stata_logname.split('.')[0] + ".log"
    os.system("cat " + stata_logname + " >> " + make_log)
    os.system("rm " + stata_logname)

    log = open(make_log, "a")
    log.write("Finished " + program + " at " + datetime.datetime.now().strftime("%m/%d/%y:%H:%M:%S") + "\n")
    log.close()
    

def getSVN(USERNAME, PASSWORD, SVNROOT, SVN_PATH, LOCAL_PATH, LOGFILE):
    os.system('''svn co --username ''' + \
              USERNAME + ''' --password ''' + \
              PASSWORD + ''' "''' + \
              SVNROOT + SVN_PATH + \
              '''" ''' + LOCAL_PATH + ''' >> ''' + LOGFILE)

def source_make(DIR, LOG, SVNMOD = False):
    make_log = open(LOG, "a")
    os.chdir("source/" + DIR)
    
    make_log.write("Running make.py for " + DIR + " at " + datetime.datetime.now().strftime("%m/%d/%y:%H:%M:%S") + "\n")
    execfile("make.py")
    make_log.write("Finished make.py for " + DIR + " at " + datetime.datetime.now().strftime("%m/%d/%y:%H:%M:%S") + "\n")
    os.system("cat ../../output/" + DIR + "/make.log >> ../../"  + LOG)
    os.chdir("../..")



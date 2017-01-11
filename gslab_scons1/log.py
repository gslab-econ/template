import os
import sys
import shutil
import subprocess
from datetime import datetime
from sys import platform
from misc import is_unix, check_lfs


def start_log(log = 'sconstruct.log'):
    '''Begins logging a build process'''
    check_lfs()
    if is_unix():
        sys.stdout = os.popen('tee %s' % log, 'wb')
    elif platform == 'win32':
        sys.stdout = open(log, 'wb')
    sys.stderr = sys.stdout 
    return None


def log_timestamp(start_time, end_time, filename):
    '''Adds beginning and ending times to a log file.'''
    with open(filename, mode = 'r+U') as f:
        content = f.read()
        f.seek(0, 0)
        f.write('Log created:    ' + start_time + '\n' + 
                'Log completed:  ' + end_time   + '\n \n' + content)
    return None

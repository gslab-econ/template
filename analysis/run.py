import sys
import subprocess

execute_script = 'source/prepare_data/create_data.r'

def main(execute_script):
    '''
    Execute scons-local script.
    Pass on command line arguments from this script's execution.
    '''
    # Pass on command line args
    del sys.argv[0]
    cl_args = ' '.join(sys.argv)

    # Create call
    call = 'Rscript %s %s' % (execute_script, cl_args)

    # Execute
    subprocess.call(call, shell = True)

main(execute_script)

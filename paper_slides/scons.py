import sys
import subprocess

def main():
    # Pass on command line args
    del sys.argv[0]
    cl_args = ' '.join(sys.argv)
    
    # Create call
    call = 'python ../config/scons/scons.py %s' % cl_args
    
    # Execute
    subprocess.call(call, shell = True)

main()

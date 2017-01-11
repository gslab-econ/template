#! /usr/bin/env python
import argparse, pdb

parser = argparse.ArgumentParser()    
parser.add_argument('-i', dest='input', nargs='+')
args = parser.parse_args()

if args.input:
    message = args.input
else:
    message = 'Test Output \n'
output_name = 'output.txt'
outfile = open(output_name, 'wb')
outfile.write( ''.join(message) )
outfile.close()

print "Test script complete"
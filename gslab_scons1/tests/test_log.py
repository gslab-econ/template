#! /usr/bin/env python

import unittest
import sys
import os

# Ensure that Python can find and load the GSLab libraries
os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append('../..')

from gslab_scons import log_timestamp


class test_log(unittest.TestCase):

    def test_start_log(self):
        pass

    def test_log_timestamp(self):
        '''Test that log_timestamp() correctly adds start/end times to a log'''
        # Write the test log file and use log_timestamp() to add 
        # stand-in starting and ending time messages.
        with open('test.txt', 'wb') as f:
            f.write('TEST CONTENT')
    	log_timestamp('test_time_start', 'test_time_end', 'test.txt')
        
        # Read the test log file and ensure log_timestamp() worked
        # as intended.
        with open('test.txt', 'rU') as f:
            content = f.read()
        self.assertEqual(content, 'Log created:    ' + 'test_time_start'+ '\n' + 
                                  'Log completed:  ' + 'test_time_end'  + '\n \n' + 
                                  'TEST CONTENT')
        os.remove('test.txt')
       

if __name__ == '__main__':
    os.getcwd()
    unittest.main()

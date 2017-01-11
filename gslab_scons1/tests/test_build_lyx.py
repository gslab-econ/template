#! /usr/bin/env python

import unittest
import sys
import os
import shutil

# Ensure that Python can find and load the GSLab libraries
os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append('../..')

from gslab_scons import build_lyx
from gslab_scons._exception_classes import BadExtensionError
from gslab_make.tests import nostderrout


class test_build_lyx(unittest.TestCase):

    def setUp(self):
        if not os.path.exists('./build/'):
            os.mkdir('./build/')

    def test_default(self):
        env = ''
        build_lyx('./build/lyx.pdf', './input/lyx_test_file.lyx', env)
        logfile_data = open('./build/sconscript.log', 'rU').read()
        self.assertIn('Log created:', logfile_data)
        if os.path.isfile('./build/sconscript.log'):
            os.remove('./build/sconscript.log')
    
    def test_bad_extension(self):
        '''Test that build_lyx() recognises an inappropriate file extension'''
        env = ''
        with self.assertRaises(BadExtensionError), nostderrout():
            build_lyx('./build/lyx.pdf', 
                      ['bad', './input/lyx_test_file.lyx'], env)
   
    def tearDown(self):
        if os.path.exists('./build/'):
            shutil.rmtree('./build/')
        if os.path.exists('output.txt'):
            os.remove('output.txt')
         
                
if __name__ == '__main__':
    os.getcwd()
    unittest.main()

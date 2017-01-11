#! /usr/bin/env python
import unittest
import sys
import os
import shutil

sys.path.append('../..')
from gslab_scons import build_python
from gslab_scons._exception_classes import BadExtensionError


class testbuild_python(unittest.TestCase):

    def setUp(self):
        if not os.path.exists('../build/'):
            os.mkdir('../build/')

    def test_default(self):
        env = ''
        build_python('../build/py.py', './input/python_test_script.py', env)
        logfile_data = open('../build/sconscript.log', 'rU').read()
        self.assertIn('Log created:', logfile_data)
        if os.path.isfile('../build/sconscript.log'):
            os.remove('../build/sconscript.log')
 
    def test_bad_extension(self):
        env = ''
        with self.assertRaises(BadExtensionError):
            build_python('../build/py.py', 
                         ['bad', './input/python_test_script.py'], 
                         env)
   
    def tearDown(self):
        if os.path.exists('../build/'):
            shutil.rmtree('../build/')
        if os.path.exists('output.txt'):
            os.remove('output.txt')


if __name__ == '__main__':
    os.getcwd()
    unittest.main()

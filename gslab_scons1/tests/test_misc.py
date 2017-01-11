#! /usr/bin/env python
import unittest
import sys
import os
import re

# Ensure that Python can find and load the GSLab libraries
os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append('../..')

import gslab_scons
import gslab_scons.misc as misc
from gslab_scons._exception_classes import BadExtensionError
from gslab_make.tests import nostderrout


class test_misc(unittest.TestCase):

    def test_check_lfs(self):
		pass

    @unittest.skipIf(sys.platform.startswith("win"), 
        "skipped test_stata_command_unix because on a windows machine")
    def test_stata_command_unix(self):
    	output = misc.stata_command_unix('flavor')
    	if sys.platform == 'darwin':
    		option = '-e'
    	else:
    		option = '-b'
    	self.assertEqual(output, 'flavor %s' % (option) + ' %s ')

    @unittest.skipUnless(sys.platform.startswith("win"), 
        "skipped test_stata_command_win because on a unix machine")
    def test_stata_command_win(self):
    	output = misc.stata_command_win('flavor')
    	self.assertEqual(output, 'flavor %s' % ('/e do') + ' %s ')

    def test_is_unix(self):
    	self.assertEqual(misc.is_unix(), not sys.platform.startswith("win"))

    def test_is_64_windows(self):
    	pass

    @unittest.skipIf(sys.platform.startswith("win"), 
    "skipped test_is_in_path because on a windows machine")
    def test_is_in_path(self):
    	self.assertEqual(misc.is_in_path('jabberwocky_long_program_name_that_fails'), None)
    	self.assertTrue(re.search('python', misc.is_in_path('python')))

    @unittest.skipIf(sys.platform.startswith("win"), 
    "skipped test_is_exe because on a windows machine")
    def test_is_exe(self):
    	pyth_exec = misc.is_in_path('python')
    	self.assertTrue(misc.is_exe(pyth_exec))
    	self.assertFalse(misc.is_exe('BAD_EXEC_FILE'))

    def test_make_list_if_string(self):
    	self.assertEqual(misc.make_list_if_string(['test', 'test']), ['test', 'test'])
    	self.assertEqual(misc.make_list_if_string('test'), ['test'])
    	self.assertEqual(misc.make_list_if_string(['test']), ['test'])

    def test_check_code_extension(self):
        '''Unit tests for check_code_extension()

        This method tests that check_code_extensions() associates software with 
        file extensions as intended.
        '''
    	self.assertEqual(misc.check_code_extension('test.do',  'stata'),  None)
    	self.assertEqual(misc.check_code_extension('test.r',   'r'),      None)
    	self.assertEqual(misc.check_code_extension('test.lyx', 'lyx'),    None)
    	self.assertEqual(misc.check_code_extension('test.py',  'python'), None)
    	
        with self.assertRaises(BadExtensionError), nostderrout():
    		misc.check_code_extension('test.badextension', 'python')

    def test_current_time(self):
        '''Test that current_time() prints times in the expected format'''
    	the_time = misc.current_time()
    	self.assertTrue(re.search('\d+-\d+-\d+\s\d+:\d+:\d+', the_time))
    

if __name__ == '__main__':
    os.getcwd()
    unittest.main()

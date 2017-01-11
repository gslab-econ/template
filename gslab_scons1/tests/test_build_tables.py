#! /usr/bin/env python
import unittest
import sys
import os
import shutil
import re

# Ensure that Python can find and load the GSLab libraries
os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append('../..')

from gslab_scons import build_tables
from gslab_scons._exception_classes import BadExtensionError
from gslab_make.tests import nostderrout


class test_build_tables(unittest.TestCase):

    def setUp(self):
        if not os.path.exists('./build/'):
            os.mkdir('./build/')

    def test_default(self):
        '''
        Test that build_tables() constructs LyX tables correctly when
        its target argument is a list
        '''

        # Specify the sources and the target before calling the build function.
        source = ['./input/tablefill_template.lyx', 
                  './input/tables_appendix.txt', 
                  './input/tables_appendix_two.txt']
        target = ['./build/tablefill_template_filled.lyx']
        build_tables(target, source, '')

        # Read the empty and filled template files
        with open('./input/tablefill_template.lyx', 'rU') as template_file:
            tag_data = template_file.readlines()
        with open('./build/tablefill_template_filled.lyx', 'rU') as table_file:
            filled_data = table_file.readlines()

        # The filled LyX file should be longer than its template by a fixed 
        # number of lines because build_tables() adds a note to this template
        # in addition to filling it in.
        self.assertEqual(len(tag_data) + 13, len(filled_data))

        # Check that build_tables() filled the template's tags correctly.
        for n in range(len(tag_data)):
            self.tag_compare(tag_data[n], filled_data[n + 13])         
 
    def test_default_string_target(self):
        '''
        Test that build_tables() constructs LyX tables correctly when
        its target argument is a string.
        '''
        
        # Specify the sources and the target before calling the build function.
        source = ['./input/tablefill_template.lyx', 
                  './input/tables_appendix.txt', 
                  './input/tables_appendix_two.txt']
        target = './build/tablefill_template_filled.lyx'
        build_tables(target, source, '')

        # Read the empty and filled template files
        with open('./input/tablefill_template.lyx', 'rU') as template_file:
            tag_data = template_file.readlines()
        with open('./build/tablefill_template_filled.lyx', 'rU') as table_file:
            filled_data = table_file.readlines()

        self.assertEqual(len(tag_data) + 13, len(filled_data))

        for n in range(len(tag_data)):
            self.tag_compare(tag_data[n], filled_data[n + 13])         

    def test_target_extension(self):
        '''Test that build_tables() recognises an inappropriate file extension'''

        # Specify the sources and the target.
        source = ['./input/tablefill_template.lyx', 
                  './input/tables_appendix.txt', 
                  './input/tables_appendix_two.txt']
        target =  './build/tablefill_template_filled.BAD'
        
        # Calling build_tables() with a target argument whose file extension
        # is unexpected should raise a BadExtensionError.
        with self.assertRaises(BadExtensionError), nostderrout():
            build_tables(target, source, '')    

    def tag_compare(self, tag_line, filled_line):
        '''
        Check that a line in a template LyX file containing a tag was
        properly filled by build_tables()
        '''
        if re.match('^.*#\d+#', tag_line) or re.match('^.*#\d+,#', tag_line):
            entry_tag = re.split('#', tag_line)[1]
            decimal_places = int(entry_tag.replace(',', ''))
            
            if decimal_places > 0:
                self.assertTrue(re.search('\.', filled_line))
                decimal_part = re.split('\.', filled_line)[1]
                non_decimal = re.compile(r'[^\d.]+')
                decimal_part = non_decimal.sub('', decimal_part)
                self.assertEqual(len(decimal_part), decimal_places)
            else:
                self.assertFalse(re.search('\.', filled_line))
            
            if re.match('^.*#\d+,#', tag_line):
                integer_part = re.split('\.', filled_line)[0]
                if len(integer_part) > 3:
                    self.assertEqual(integer_part[-4], ',')
    
    def tearDown(self):
        if os.path.exists('./build/'):
            shutil.rmtree('./build/')
        

if __name__ == '__main__':
    os.getcwd()
    unittest.main()

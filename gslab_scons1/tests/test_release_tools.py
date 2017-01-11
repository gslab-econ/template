import unittest
import sys
import os
import re
import mock
import tempfile
import shutil

# Ensure that Python can find and load the GSLab libraries
os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append('../..')

import gslab_scons
import gslab_scons._release_tools as tools
from gslab_scons._exception_classes import ReleaseError
from gslab_make.tests import nostderrout


class TestReleaseTools(unittest.TestCase):

    @mock.patch('gslab_scons._release_tools.requests.session')
    @mock.patch('gslab_scons._release_tools.open')
    @mock.patch('gslab_scons._release_tools.os.path.isfile')
    def test_upload_asset_standard(self, mock_isfile, mock_open, mock_session):
        '''
        Test that upload_asset() correctly prepares a request
        to upload a release asset to GitHub.
        '''
        # Allow upload_asset() to work without an actual release asset file
        mock_isfile.return_value = True
        mock_open.return_value   = 'file_object'

        # There are three connected requests-related mocks at play here:
        # i) mock_session: the requests.session() function
        # ii) the session object returned by requests.session
        # iii) the mocked post() method of the mocked session object
        mock_session.return_value = mock.MagicMock(post = mock.MagicMock())

        tools.upload_asset(token        = 'test_token', 
                           org          = 'gslab-econ', 
                           repo         = 'gslab_python', 
                           release_id   = 'test_release', 
                           file_name    = 'release.txt', 
                           content_type = 'text/markdown')

        # Check that upload_asset called a session object's post() method
        # once and with the correct arguments.
        mock_session.return_value.post.assert_called_once()

        keyword_args    = mock_session.return_value.post.call_args[1]
        positional_args = mock_session.return_value.post.call_args[0]

        self.assertEqual(keyword_args['files']['file'],            'file_object')
        self.assertEqual(keyword_args['headers']['Authorization'], 'token test_token')
        self.assertEqual(keyword_args['headers']['Content-Type'],  'text/markdown')
        
        # Check that the first positional argument matches the desired upload path
        desired_upload_path = ''.join(['https://uploads.github.com/repos/',
                                       'gslab-econ/gslab_python/releases/',
                                       'test_release/assets?name=release.txt'])
        self.assertEqual(positional_args[0], desired_upload_path)

    @mock.patch('gslab_scons._release_tools.requests.session')
    def test_upload_asset_bad_file(self, mock_session):
        '''
        Test that upload_asset() raises an error when its file_name
        argument isn't valid.
        '''
        mock_session.return_value = mock.MagicMock(post = mock.MagicMock())

        with self.assertRaises(ReleaseError), nostderrout():
            tools.upload_asset(token        = 'test_token', 
                               org          = 'gslab-econ', 
                               repo         = 'gslab_python', 
                               release_id   = 'test_release', 
                               file_name    = 'nonexistent_file', 
                               content_type = 'text/markdown')

    @mock.patch('gslab_scons._release_tools.subprocess.call')
    def test_up_to_date(self, mock_call):
        '''
        Test that up_to_date() correctly recognises
        an SCons directory as up-to-date or out of date.
        '''
        # The mock of subprocess call should write pre-specified text
        # to stdout. This mock prevents us from having to set up real
        # SCons and git directories.
        mock_call.side_effect = self.make_call_side_effect('Your branch is up-to-date')
        self.assertTrue(gslab_scons._release_tools.up_to_date(mode = 'git'))
        mock_call.side_effect = self.make_call_side_effect('modified:   .sconsign.dblite')
        self.assertFalse(gslab_scons._release_tools.up_to_date(mode = 'git'))

        mock_call.side_effect = self.make_call_side_effect("scons: `.' is up to date.")
        self.assertTrue(gslab_scons._release_tools.up_to_date(mode = 'scons'))
        mock_call.side_effect = self.make_call_side_effect('python some_script.py')
        self.assertFalse(gslab_scons._release_tools.up_to_date(mode = 'scons'))

        # The up_to_date() function shouldn't work in SCons or git mode
        # when it is called outside of a SCons directory or a git 
        # repository, respectively.       
        mock_call.side_effect = self.make_call_side_effect("Not a git repository")
        with self.assertRaises(ReleaseError), nostderrout():
            gslab_scons._release_tools.up_to_date(mode = 'git')

        mock_call.side_effect = self.make_call_side_effect("No SConstruct file found")
        with self.assertRaises(ReleaseError), nostderrout():
            gslab_scons._release_tools.up_to_date(mode = 'scons')   

    @staticmethod
    def make_call_side_effect(text):
        '''
        Return a side effect to be used with mock that
        prints text to a file specified as the stderr
        argument of function being mocked.
        '''
        def side_effect(*args, **kwargs):
            log = kwargs['stdout']
            log.write(text)
            
        return side_effect

    def test_extract_dot_git(self):
        '''
        Test that extract_dot_git() correctly extracts repository
        information from a .git folder's config file.
        '''
        test_dir  = os.path.dirname(os.path.realpath(__file__))
        git_dir   = os.path.join(test_dir, '../../.git')
        repo_info = tools.extract_dot_git(git_dir)
        self.assertEqual(repo_info[0], 'gslab_python')
        self.assertEqual(repo_info[1], 'gslab-econ')

        # Ensure that extract_dot_git() raises an error the directory
        # argument is not a .git folder.
        # i) The directory argument identifies an empry folder
        temp_dir = tempfile.mkdtemp()
        with self.assertRaises(ReleaseError), nostderrout():
            repo_info = tools.extract_dot_git(test_dir)
        os.rmdir(temp_dir)
        # ii) The directory argument does not identify a real directory
        with self.assertRaises(ReleaseError), nostderrout():
            repo_info = tools.extract_dot_git('Not a directory')

    def test_create_size_dictionary(self):
        '''
        Test that create_size_dictionary() correctly reports
        files' sizes in bytes.
        '''
        test_dir = os.path.dirname(os.path.realpath(__file__))
        test_dir = os.path.join(test_dir, 'input/size_test') 
        sizes    = tools.create_size_dictionary(test_dir)

        # Check that test.txt and test.jpg are in the dictionary
        txt_path = [path for path in sizes.keys() if re.search('test.txt$', path)]
        jpg_path = [path for path in sizes.keys() if re.search('test.jpg$', path)]

        self.assertTrue(bool(txt_path))
        self.assertTrue(bool(jpg_path))

        # Check that the size dictionary reports these files' correct sizes in bytes
        self.assertEqual(sizes[txt_path[0]], 93)
        self.assertEqual(sizes[jpg_path[0]], 149084)

        # Check that the function raises an error when its path argument
        # is not a directory.
        with self.assertRaises(ReleaseError), nostderrout():
            sizes = tools.create_size_dictionary('Not a directory')
        # The path argument must be a string
        with self.assertRaises(TypeError), nostderrout():
            sizes = tools.create_size_dictionary(10)


if __name__ == '__main__':
    os.getcwd()
    unittest.main()

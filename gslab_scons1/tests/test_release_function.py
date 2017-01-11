import unittest
import sys
import os
import re
import mock
import shutil
import requests

# Ensure that Python can find and load the GSLab libraries
os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append('../..')

import gslab_scons
import gslab_scons._release_tools as tools
from gslab_scons._exception_classes import ReleaseError
from gslab_make.tests import nostderrout


class TestReleaseFunction(unittest.TestCase):

    @mock.patch('gslab_scons._release_tools.upload_asset')
    @mock.patch('gslab_scons._release_tools.requests.session')
    @mock.patch('gslab_scons._release_tools.getpass.getpass')
    @mock.patch('gslab_scons._release_tools.time.sleep') # For skipping time delay
    @mock.patch('gslab_scons._release_tools.os.makedirs')
    @mock.patch('gslab_scons._release_tools.os.path.isdir')
    @mock.patch('gslab_scons._release_tools.shutil.rmtree')
    @mock.patch('gslab_scons._release_tools.shutil.copy')
    @mock.patch('gslab_scons._release_tools.shutil.make_archive')
    @mock.patch('gslab_scons._release_tools.shutil.move')
    def test_release_standard(self, mock_move, mock_make_archive, mock_copy, 
                              mock_rmtree, mock_isdir, mock_makedirs, 
                              mock_sleep, mock_getpass, mock_session,
                              mock_upload):
        '''
        Test that release() correctly prepares a release
        that uploads zipped files to Google Drive.
        '''
        # Mock functions called by release() to simulate an actual call
        mock_getpass.return_value = 'test_token'
        mock_session.return_value = mock.MagicMock(post = mock.MagicMock(),
                                                   get  = mock.MagicMock())
        mock_session.return_value.get.return_value.content = self.return_mock_release_data()
        # When org/repo refers to a nonexistent GitHub repository, 
        # make the release request fail. 
        mock_session.return_value.post.side_effect = self.post_side_effect

        # Add a side effect to mock_upload to preserve a listing of release assets
        mock_upload.side_effect = self.upload_asset_side_effect

        DriveReleaseFiles = ['paper.pdf', 'plot.pdf']
        tools.release('test_version', 
                      DriveReleaseFiles = DriveReleaseFiles, 
                      local_release     = 'Google Drive/release/local_release/', 
                      org               = 'org', 
                      repo              = 'repo', 
                      target_commitish  = 'test_branch', 
                      zip_release       = True)

        mock_session.return_value.post.assert_called_once()
        post_args = mock_session.return_value.post.call_args

        # Check that the first positional argument of session.post() is 
        # the url to which we desire to make our release.
        desired_release_url = 'https://test_token:@api.github.com/repos/org/repo/releases'
        self.assertEqual(post_args[0][0], desired_release_url)

        # Check that the correct data was passed to session.post()
        data = post_args[1]['data']
        self.assertTrue(re.search('"body": ""', data))
        self.assertTrue(re.search('"name": "test_version"', data))
        self.assertTrue(re.search('"target_commitish": "test_branch"', data))
        self.assertTrue(re.search('"tag_name": "test_version"', data))
        self.assertTrue(re.search('"prerelease": false', data))
        self.assertTrue(re.search('"draft": false', data))

        # Check that release() called upload_asset() with the correct arguments
        mock_upload.assert_called_once()
        # We expect test_ID to be the release ID given the mocked-up return value
        # of session.get()
        self.assertEqual(mock_upload.call_args[1]['release_id'], 'test_ID')

        # Check that release() zipped the files released to Google Drive correctly...
        mock_copy.assert_any_call('paper.pdf', 'release_content/paper.pdf')
        mock_copy.assert_any_call('plot.pdf',  'release_content/plot.pdf')
        mock_make_archive.assert_called_with('release_content', 'zip', 'release_content')
        # ...and moved them to the local_release Google Drive directory
        mock_move.assert_called_with('release_content.zip', 
                                     'Google Drive/release/local_release/release.zip')
        # Check that the assets listed in the file whose path is
        # passed to upload_asset() are those specified by release()'s 
        # DriveReleaseFiles argument.
        with open('assets_listing.txt', 'rU') as assets:
            lines = assets.readlines()
        self.assertIn(lines[1].strip(), DriveReleaseFiles)
        self.assertIn(lines[2].strip(), DriveReleaseFiles)

        os.remove('assets_listing.txt')

    @staticmethod
    def return_mock_release_data():
        '''This is mocked-up output from session.get(path)'''
        return  ','.join([
                '[{"url":"https://api.github.com/repos/org/repo/releases/test_ID"',
                 '"assets_url":"https://api.github.com/repos/org/repo/releases/test_ID/assets"',
                 '"upload_url":"https://uploads.github.com/repos/org/repo/releases/test_ID/assets{?name,label}"',
                 '"html_url":"https://github.com/org/repo/releases/tag/test_version"',
                 '"id":test_ID',
                 '"tag_name":"test_version"',
                 '"target_commitish":"test_branch"',
                 '"name":"test_version"',
                 '"draft":false',
                 '"prerelease":false}]'])

    @staticmethod
    def upload_asset_side_effect(*args, **kwargs):
        '''
        This side effect, intended for use with a mock of upload_asset, 
        copird the uploaded asset so that a version will remain to be checked 
        by unit tests. 
        '''
        assets_path    = kwargs['file_name']
        shutil.copyfile(assets_path, 'assets_listing.txt')    


    @staticmethod
    def post_side_effect(*args, **kwargs):
      '''
      This side effect returns a MagicMock that raises an error 
      when its raise_for_status() method is called unless
      a specific release_path is specified and there if a 
      valid tag_name
      '''
      # The release path is specified by the first positional argument.
      mock_output = mock.MagicMock(raise_for_status = mock.MagicMock())
      release_path = args[0]
      real_path = "https://test_token:@api.github.com/repos/org/repo/releases"

      def raise_http_error():
          raise requests.exceptions.HTTPError('404 Client Error')

      if release_path != real_path:
          mock_output.raise_for_status.side_effect = raise_http_error

      return mock_output  

    @mock.patch('gslab_scons._release_tools.upload_asset')
    @mock.patch('gslab_scons._release_tools.requests.session')
    @mock.patch('gslab_scons._release_tools.getpass.getpass')
    @mock.patch('gslab_scons._release_tools.time.sleep') 
    @mock.patch('gslab_scons._release_tools.os.makedirs')
    @mock.patch('gslab_scons._release_tools.os.path.isdir')
    @mock.patch('gslab_scons._release_tools.shutil.rmtree')
    @mock.patch('gslab_scons._release_tools.shutil.copy')
    @mock.patch('gslab_scons._release_tools.shutil.make_archive')
    @mock.patch('gslab_scons._release_tools.shutil.move')
    def test_release_nozip(self, mock_move, mock_make_archive, mock_copy, 
                           mock_rmtree, mock_isdir, mock_makedirs, 
                           mock_sleep, mock_getpass, mock_session,
                           mock_upload):
        '''
        Test that release() correctly prepares a release
        that uploads unzipped files to Google Drive.
        '''
        # Mock functions called by release() to simulate an actual call
        mock_getpass.return_value = 'test_token'
        mock_session.return_value.get.return_value.content = self.return_mock_release_data()

        DriveReleaseFiles = ['paper.pdf', 'plot.pdf']
        tools.release('test_version', 
                      DriveReleaseFiles = DriveReleaseFiles, 
                      local_release     = 'Google Drive/release/local_release/', 
                      org               = 'org', 
                      repo              = 'repo', 
                      target_commitish  = 'test_branch', 
                      zip_release       = False)
        # The release() call should not have created a zip archive...
        mock_make_archive.assert_not_called()
        # ...but it should have moved the release files into the local_release directory.
        mock_copy.assert_any_call('paper.pdf', 'Google Drive/release/local_release/paper.pdf')
        mock_copy.assert_any_call('plot.pdf',  'Google Drive/release/local_release/plot.pdf')

    @mock.patch('gslab_scons._release_tools.upload_asset')
    @mock.patch('gslab_scons._release_tools.requests.session')
    @mock.patch('gslab_scons._release_tools.getpass.getpass')
    @mock.patch('gslab_scons._release_tools.os.makedirs')
    @mock.patch('gslab_scons._release_tools.os.path.isdir')
    @mock.patch('gslab_scons._release_tools.shutil.rmtree')
    @mock.patch('gslab_scons._release_tools.shutil.copy')
    @mock.patch('gslab_scons._release_tools.shutil.make_archive')
    @mock.patch('gslab_scons._release_tools.shutil.move')
    def test_release_no_drive(self, mock_move, mock_make_archive, mock_copy, 
                              mock_rmtree, mock_isdir, mock_makedirs, 
                              mock_getpass, mock_session,
                              mock_upload):
        '''
        Test that release() correctly prepares a release
        that does not upload files to Google Drive.
        '''
        # Mock functions called by release() to simulate an actual call
        mock_session.return_value.get.return_value.content = self.return_mock_release_data()

        # Test without DriveReleaseFiles
        tools.release('test_version', 
                      DriveReleaseFiles = [], 
                      local_release     = 'Google Drive/release/local_release/', 
                      org               = 'org', 
                      repo              = 'repo', 
                      target_commitish  = 'test_branch')
        # Check that no file operations occur when no files are specified for release
        # to Google Drive.
        mock_copy.assert_not_called()      
        mock_makedirs.assert_not_called()
        mock_rmtree.assert_not_called()
        mock_make_archive.assert_not_called()
        mock_move.assert_not_called()
        mock_upload.assert_not_called()    

    @mock.patch('gslab_scons._release_tools.upload_asset')
    @mock.patch('gslab_scons._release_tools.requests.session')
    @mock.patch('gslab_scons._release_tools.getpass.getpass')
    @mock.patch('gslab_scons._release_tools.time.sleep') 
    @mock.patch('gslab_scons._release_tools.os.makedirs')
    @mock.patch('gslab_scons._release_tools.os.path.isdir')
    @mock.patch('gslab_scons._release_tools.shutil.rmtree')
    @mock.patch('gslab_scons._release_tools.shutil.copy')
    @mock.patch('gslab_scons._release_tools.shutil.make_archive')
    @mock.patch('gslab_scons._release_tools.shutil.move')
    def test_release_unintended_inputs(self, mock_move, mock_make_archive, mock_copy, 
                                       mock_rmtree, mock_isdir, mock_makedirs, 
                                       mock_sleep, mock_getpass, mock_session,
                                       mock_upload):
        '''
        Test that release() responds as expected to 
        unintended inputs.
        '''
        # Mock functions called by release() to simulate an actual call
        mock_getpass.return_value = 'test_token'
        mock_session.return_value.get.return_value.content = self.return_mock_release_data()
        mock_session.return_value.post.side_effect = self.post_side_effect

        # Inappropriate local_release argument should not if the DriveReleaseFiles
        # argument is empty.
        try:
            tools.release('test_version', 
                          DriveReleaseFiles = [], 
                          local_release     = 1, 
                          org               = 'org', 
                          repo              = 'repo', 
                          target_commitish  = 'test_branch')
        except:
            self.fail("Running release() with an invalid local_release argument and without"
                      "files to be released to Google Drive shouldn't raise an error!")

        # Providing a local_release argument of an inappropriate type should
        # raise an error when we instruct release() to upload files to Google Drive
        with self.assertRaises(AttributeError), nostderrout():
            tools.release('test_version', 
                          DriveReleaseFiles = ['paper.pdf', 'plot.pdf'], 
                          local_release     = 1, 
                          org               = 'org', 
                          repo              = 'repo', 
                          target_commitish  = 'test_branch')

        # The local_release argument currently has to specify a /release/ directory.
        # Capitalisation matters!
        with self.assertRaises(ReleaseError), nostderrout():
            tools.release('test_version', 
                          DriveReleaseFiles = ['paper.pdf', 'plot.pdf'], 
                          local_release     = 'root/Release/folder', 
                          org               = 'org', 
                          repo              = 'repo', 
                          target_commitish  = 'test_branch')   

        # When org/repo refers to a nonexistent GitHub repository, the  
        # release request will fail. This should raise a requests error.
        with self.assertRaises(requests.exceptions.HTTPError), nostderrout():
            tools.release('test_version', 
                          DriveReleaseFiles = ['paper.pdf', 'plot.pdf'], 
                          local_release     = 'root/release', 
                          org               = 'orgg', # Misspelling
                          repo              = 'repo', 
                          target_commitish  = 'test_branch')  

        with self.assertRaises(requests.exceptions.HTTPError), nostderrout():
            tools.release('test_version', 
                          DriveReleaseFiles = ['paper.pdf', 'plot.pdf'], 
                          local_release     = 'root/release', 
                          org               = 'org', 
                          repo              = 1, # Wrong type
                          target_commitish  = 'test_branch')  

        # Passing a non-container, non-string value for which bool() returns True to DriveReleaseFiles
        # raises a TypeError
        with self.assertRaises(TypeError), nostderrout():
            tools.release('test_version', 
                          DriveReleaseFiles = True, 
                          local_release     = 'root/release/repo-test_branch', 
                          org               = 'org', 
                          repo              = 'repo', 
                          target_commitish  = 'test_branch')    

        # Passing a container holding non-string objects to DriveReleaseFiles
        # raises an AttributeError
        with self.assertRaises(AttributeError), nostderrout():
            tools.release('test_version', 
                          DriveReleaseFiles = [1, 2, 3], 
                          local_release     = 'root/release/repo-test_branch', 
                          org               = 'org', 
                          repo              = 'repo', 
                          target_commitish  = 'test_branch')  


if __name__ == '__main__':
    os.getcwd()
    unittest.main()

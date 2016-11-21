from __future__ import absolute_import

import unittest
from mock import call, mock

from gcptools.create_projects import create_project
from gcptools.create_projects import create_service_accounts

# Super useful links about testing
#
# http://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure
# https://www.toptal.com/python/an-introduction-to-mocking-in-python
# https://docs.python.org/2/library/pdb.html
#
# import pdb; pdb.set_trace()
#
class CreateProjectsTest(unittest.TestCase):

    @mock.patch('gcptools.create_projects.google')
    def test_create_project_with_organization(self, mock_google):
    # def test_create_project_with_organization(self):
        project_id = 1
        settings = {
            'organization': 'Broad',
            'folder': 'someFolder'
        }
        create_project(project_id, settings)
        mock_google.create_project.assert_called_with({'projectId': 1, 'name': 1, 'parent': {'type': 'organization', 'id': 'Broad'}})

    @mock.patch('gcptools.create_projects.google')
    def test_create_project_with_folder(self, mock_google):
    # def test_create_project_with_folder(self):
        project_id = 1
        settings = {
            'organization': 'Broad',
            'folder': 'someFolder'
        }
        create_project(project_id, settings)
        mock_google.create_project.assert_called_with({'projectId': 1, 'name': 1, 'parent': {'type': 'organization', 'id': 'Broad'}})

    @mock.patch('gcptools.create_projects.google')
    def test_create_service_accounts(self, mock_google):
    # def test_create_service_accounts(self):
        project_id = 1
        settings = {
            'service_accounts': [1,2]
        }
        create_service_accounts(project_id, settings)
        mock_google.create_service_account.assert_has_calls([call(1,1), call(1,2)], any_order=True)

if __name__ == '__main__':
	unittest.main()

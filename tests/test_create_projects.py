from __future__ import absolute_import

import mock
import unittest

from gcptools.create_projects import create_project

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
    def testCreateProjectWithOrganization(self, mock_google):
    # def testCreateProject(self):
        project_id = 1
        settings = {
            'organization': 'Broad',
            'folder': 'someFolder'
        }
        create_project(project_id, settings)
        mock_google.create_project.assert_called_with({'projectId': 1, 'name': 1, 'parent': {'type': 'organization', 'id': 'Broad'}})

    @mock.patch('gcptools.create_projects.google')
    def testCreateProjectWithFolder(self, mock_google):
    # def testCreateProjectWithFolder(self):
        project_id = 1
        settings = {
            'organization': 'Broad',
            'folder': 'someFolder'
        }
        create_project(project_id, settings)
        mock_google.create_project.assert_called_with({'projectId': 1, 'name': 1, 'parent': {'type': 'organization', 'id': 'Broad'}})

if __name__ == '__main__':
	unittest.main()

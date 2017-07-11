# Copyright 2017 DataCentred Ltd
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from keystoneauth1.exceptions import http

from sentinel.tests.functional import matchers
from sentinel.tests.functional.identity import base

TEST_PROJECT = 'test'
TEST_PROJECT_DOMAIN = 'default'
TEST_PROJECT_DESCRIPTION = 'Sentinel Test Project'

TEST_NESTED_PROJECT = 'child'

class KeystoneUsersTestCase(base.KeystoneBaseTestCase):

    def test_create(self):
        project = self.sentinel.projects.create(TEST_PROJECT,
                                                TEST_PROJECT_DOMAIN,
                                                description=TEST_PROJECT_DESCRIPTION)
        self.addCleanup(self.sentinel.projects.delete, project)
        self.assertEqual(project.name, TEST_PROJECT)
        self.assertEqual(project.description, TEST_PROJECT_DESCRIPTION)
        self.assertEqual(project.enabled, True)
        self.assertNotEqual(project.domain_id, TEST_PROJECT_DOMAIN)
        self.assertRaises(http.Conflict, self.sentinel.projects.create, TEST_PROJECT, 'default')

    def test_nested_create(self):
        parent = self.sentinel.projects.create(TEST_PROJECT,
                                               TEST_PROJECT_DOMAIN)
        self.addCleanup(self.sentinel.projects.delete, parent)
        child = self.sentinel.projects.create(TEST_NESTED_PROJECT,
                                              TEST_PROJECT_DOMAIN,
                                              parent=parent)
        self.addCleanup(self.sentinel.projects.delete, child)
        self.assertEqual(child.parent_id, parent.id)

    def test_update(self):
        project = self.sentinel.projects.create(TEST_PROJECT,
                                                TEST_PROJECT_DOMAIN)
        self.addCleanup(self.sentinel.projects.delete, project)
        project = self.sentinel.projects.update(project,
                                                description=TEST_PROJECT_DESCRIPTION,
                                                enabled=False)
        self.assertEqual(project.description, TEST_PROJECT_DESCRIPTION)
        self.assertEqual(project.enabled, False)

    def test_nested_get(self):
        parent = self.sentinel.projects.create(TEST_PROJECT,
                                               TEST_PROJECT_DOMAIN)
        self.addCleanup(self.sentinel.projects.delete, parent)
        child = self.sentinel.projects.create(TEST_NESTED_PROJECT,
                                              TEST_PROJECT_DOMAIN,
                                              parent=parent)
        self.addCleanup(self.sentinel.projects.delete, child)
        project = self.sentinel.projects.get(parent, subtree_as_ids=True)
        self.assertIn(child.id, project.subtree)
        project = self.sentinel.projects.get(child, parents_as_ids=True)
        self.assertIn(parent.id, project.parents)

    def test_list(self):
        sp_project = self.keystone.projects.create(TEST_PROJECT,
                                                   TEST_PROJECT_DOMAIN)
        self.addCleanup(self.keystone.projects.delete, sp_project)
        project = self.sentinel.projects.create(TEST_PROJECT,
                                                TEST_PROJECT_DOMAIN)
        self.addCleanup(self.sentinel.projects.delete, project)
        projects = self.sentinel.projects.list()
        self.assertThat(project, matchers.IsInCollection(projects))
        self.assertThat(sp_project, matchers.IsNotInCollection(projects))

# vi: ts=4 et:

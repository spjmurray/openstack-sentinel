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

from sentinel.tests.functional import base, matchers
from sentinel.tests.functional import client_fixtures as fixtures

TEST_PROJECT = 'test'
TEST_PROJECT_DOMAIN = 'default'
TEST_PROJECT_DESCRIPTION = 'Sentinel Test Project'


class KeystoneUsersTestCase(base.BaseTestCase):

    def test_create(self):
        project = self.sentinel.identity.projects.create(
            TEST_PROJECT,
            TEST_PROJECT_DOMAIN,
            description=TEST_PROJECT_DESCRIPTION)
        self.addCleanup(self.sentinel.identity.projects.delete, project)
        self.assertEqual(project.name, TEST_PROJECT)
        self.assertEqual(project.description, TEST_PROJECT_DESCRIPTION)
        self.assertEqual(project.enabled, True)
        self.assertNotEqual(project.domain_id, TEST_PROJECT_DOMAIN)

    def test_create_conflict(self):
        project = self.useFixture(fixtures.Project(self.sentinel))
        self.assertRaises(
            http.Conflict,
            self.sentinel.identity.projects.create,
            project.entity.name,
            'default')

    def test_nested_create(self):
        parent = self.useFixture(fixtures.Project(self.sentinel))
        child = self.useFixture(fixtures.Project(self.sentinel, parent=parent))
        self.assertEqual(child.entity.parent_id, parent.entity.id)

    def test_update(self):
        project_fix = self.useFixture(fixtures.Project(self.sentinel))
        project = self.sentinel.identity.projects.update(
            project_fix.entity,
            description=TEST_PROJECT_DESCRIPTION,
            enabled=False)
        self.assertEqual(project.description, TEST_PROJECT_DESCRIPTION)
        self.assertEqual(project.enabled, False)

    def test_update_taint(self):
        project = self.useFixture(fixtures.Project(self.openstack))
        self.assertRaises(
            http.Forbidden,
            self.sentinel.identity.projects.update,
            project.entity,
            description=TEST_PROJECT_DESCRIPTION)

    def test_get(self):
        project = self.useFixture(fixtures.Project(self.sentinel))
        self.sentinel.identity.projects.get(project.entity)

    def test_get_taint(self):
        project = self.useFixture(fixtures.Project(self.openstack))
        self.assertRaises(http.Forbidden, self.sentinel.identity.projects.get, project.entity)

    def test_nested_get(self):
        parent = self.useFixture(fixtures.Project(self.sentinel))
        child = self.useFixture(fixtures.Project(self.sentinel, parent=parent))
        project = self.sentinel.identity.projects.get(parent.entity, subtree_as_ids=True)
        self.assertIn(child.entity.id, project.subtree)
        project = self.sentinel.identity.projects.get(child.entity, parents_as_ids=True)
        self.assertIn(parent.entity.id, project.parents)

    def test_list(self):
        project = self.useFixture(fixtures.Project(self.sentinel))
        projects = self.sentinel.identity.projects.list()
        self.assertThat(project.entity, matchers.IsInCollection(projects))

    def test_list_filtering(self):
        project = self.useFixture(fixtures.Project(self.openstack))
        projects = self.sentinel.identity.projects.list()
        self.assertThat(project.entity, matchers.IsNotInCollection(projects))

# vi: ts=4 et:

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

class KeystoneRolesTestCase(base.KeystoneBaseTestCase):

    def test_list(self):
        roles = self.sentinel.roles.list()
        self.assertIn('user', [r.name for r in roles])
        self.assertNotIn('admin', [r.name for r in roles])

    def test_user_role_grant(self):
        user = self.sentinel.users.create('test_user')
        self.addCleanup(self.sentinel.users.delete, user)
        project = self.sentinel.projects.create('test_project', 'test_domain')
        self.addCleanup(self.sentinel.projects.delete, project)
        roles = self.sentinel.roles.list()
        self.sentinel.roles.grant(roles[0], user=user, project=project)

    def test_user_role_check(self):
        user = self.sentinel.users.create('test_user')
        self.addCleanup(self.sentinel.users.delete, user)
        project = self.sentinel.projects.create('test_project', 'test_domain')
        self.addCleanup(self.sentinel.projects.delete, project)
        roles = self.sentinel.roles.list()
        self.sentinel.roles.grant(roles[0], user=user, project=project)
        self.sentinel.roles.check(roles[0], user=user, project=project)

    def test_user_role_revoke(self):
        user = self.sentinel.users.create('test_user')
        self.addCleanup(self.sentinel.users.delete, user)
        project = self.sentinel.projects.create('test_project', 'test_domain')
        self.addCleanup(self.sentinel.projects.delete, project)
        roles = self.sentinel.roles.list()
        self.sentinel.roles.grant(roles[0], user=user, project=project)
        self.sentinel.roles.revoke(roles[0], user=user, project=project)

    def test_user_role_list(self):
        user = self.sentinel.users.create('test_user')
        self.addCleanup(self.sentinel.users.delete, user)
        project = self.sentinel.projects.create('test_project', 'test_domain')
        self.addCleanup(self.sentinel.projects.delete, project)
        roles = self.sentinel.roles.list()
        self.sentinel.roles.grant(roles[0], user=user, project=project)
        new_roles = self.sentinel.roles.list(user=user, project=project)
        self.assertThat(roles[0], matchers.IsInCollection(new_roles))

    def test_group_role_grant(self):
        group = self.sentinel.groups.create('test_group')
        self.addCleanup(self.sentinel.groups.delete, group)
        project = self.sentinel.projects.create('test_project', 'test_domain')
        self.addCleanup(self.sentinel.projects.delete, project)
        roles = self.sentinel.roles.list()
        self.sentinel.roles.grant(roles[0], group=group, project=project)

    def test_group_role_check(self):
        group = self.sentinel.groups.create('test_group')
        self.addCleanup(self.sentinel.groups.delete, group)
        project = self.sentinel.projects.create('test_project', 'test_domain')
        self.addCleanup(self.sentinel.projects.delete, project)
        roles = self.sentinel.roles.list()
        self.sentinel.roles.grant(roles[0], group=group, project=project)
        self.sentinel.roles.check(roles[0], group=group, project=project)

    def test_group_role_revoke(self):
        group = self.sentinel.groups.create('test_group')
        self.addCleanup(self.sentinel.groups.delete, group)
        project = self.sentinel.projects.create('test_project', 'test_domain')
        self.addCleanup(self.sentinel.projects.delete, project)
        roles = self.sentinel.roles.list()
        self.sentinel.roles.grant(roles[0], group=group, project=project)
        self.sentinel.roles.revoke(roles[0], group=group, project=project)

    def test_group_role_list(self):
        group = self.sentinel.groups.create('test_group')
        self.addCleanup(self.sentinel.groups.delete, group)
        project = self.sentinel.projects.create('test_project', 'test_domain')
        self.addCleanup(self.sentinel.projects.delete, project)
        roles = self.sentinel.roles.list()
        self.sentinel.roles.grant(roles[0], group=group, project=project)
        new_roles = self.sentinel.roles.list(group=group, project=project)
        self.assertThat(roles[0], matchers.IsInCollection(new_roles))

# vi: ts=4 et:


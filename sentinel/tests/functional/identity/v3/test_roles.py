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
from sentinel.tests.functional import client_fixtures as fixtures
from sentinel.tests.functional.identity import base

class KeystoneRolesTestCase(base.KeystoneBaseTestCase):

    def test_list(self):
        roles = self.sentinel.roles.list()
        self.assertIn('user', [r.name for r in roles])
        self.assertNotIn('admin', [r.name for r in roles])

    def test_user_role_grant(self):
        user = self.useFixture(fixtures.User(self.sentinel))
        project = self.useFixture(fixtures.Project(self.sentinel))
        role = self.useFixture(fixtures.Role(self.sentinel))
        self.sentinel.roles.grant(role.entity, user=user.entity, project=project.entity)

    def test_user_role_check(self):
        grant = self.useFixture(fixtures.UserProjectGrant(self.sentinel))
        self.sentinel.roles.check(grant.role.entity, user=grant.user.entity, project=grant.project.entity)

    def test_user_role_revoke(self):
        grant = self.useFixture(fixtures.UserProjectGrant(self.sentinel))
        self.sentinel.roles.revoke(grant.role.entity, user=grant.user.entity, project=grant.project.entity)

    def test_user_role_list(self):
        grant = self.useFixture(fixtures.UserProjectGrant(self.sentinel))
        roles = self.sentinel.roles.list(user=grant.user.entity, project=grant.project.entity)
        self.assertThat(grant.role.entity, matchers.IsInCollection(roles))

    def test_group_role_grant(self):
        group = self.useFixture(fixtures.Group(self.sentinel))
        project = self.useFixture(fixtures.Project(self.sentinel))
        role = self.useFixture(fixtures.Role(self.sentinel))
        self.sentinel.roles.grant(role.entity, group=group.entity, project=project.entity)

    def test_group_role_check(self):
        grant = self.useFixture(fixtures.GroupProjectGrant(self.sentinel))
        self.sentinel.roles.check(grant.role.entity, group=grant.group.entity, project=grant.project.entity)

    def test_group_role_revoke(self):
        grant = self.useFixture(fixtures.GroupProjectGrant(self.sentinel))
        self.sentinel.roles.revoke(grant.role.entity, group=grant.group.entity, project=grant.project.entity)

    def test_group_role_list(self):
        grant = self.useFixture(fixtures.GroupProjectGrant(self.sentinel))
        roles = self.sentinel.roles.list(group=grant.group.entity, project=grant.project.entity)
        self.assertThat(grant.role.entity, matchers.IsInCollection(roles))

# vi: ts=4 et:


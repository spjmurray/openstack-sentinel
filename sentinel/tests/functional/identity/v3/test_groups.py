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


TEST_GROUP = 'sentinel-test'
TEST_GROUP_DESCRIPTION = 'Sentinel Test Group'


class KeystoneGroupsTestCase(base.BaseTestCase):

    def test_create(self):
        group = self.sentinel.identity.groups.create(
            TEST_GROUP,
            description=TEST_GROUP_DESCRIPTION)
        self.addCleanup(self.sentinel.identity.groups.delete, group)
        self.assertEqual(group.name, TEST_GROUP)
        self.assertEqual(group.description, TEST_GROUP_DESCRIPTION)
        self.assertRaises(http.Conflict, self.sentinel.identity.groups.create, TEST_GROUP)

    def test_update(self):
        group_fix = self.useFixture(fixtures.Group(self.sentinel))
        group = self.sentinel.identity.groups.update(
            group_fix.entity,
            name=TEST_GROUP,
            description=TEST_GROUP_DESCRIPTION)
        self.assertEqual(group.name, TEST_GROUP)
        self.assertEqual(group.description, TEST_GROUP_DESCRIPTION)

    def test_get(self):
        group = self.useFixture(fixtures.Group(self.sentinel))
        self.sentinel.identity.groups.get(group.entity)

    def test_delete(self):
        group = self.sentinel.identity.groups.create(TEST_GROUP)
        self.sentinel.identity.groups.delete(group)
        self.assertRaises(http.NotFound, self.sentinel.identity.groups.delete, group)

    def test_list(self):
        sp_group = self.useFixture(fixtures.Group(self.openstack))
        group = self.useFixture(fixtures.Group(self.sentinel))
        groups = self.sentinel.identity.groups.list()
        self.assertThat(group.entity, matchers.IsInCollection(groups))
        self.assertThat(sp_group.entity, matchers.IsNotInCollection(groups))

    def test_group_add_user(self):
        user = self.useFixture(fixtures.User(self.sentinel))
        group = self.useFixture(fixtures.Group(self.sentinel))
        self.sentinel.identity.users.add_to_group(user.entity, group.entity)

    def def_group_remove_user(self):
        user = self.useFixture(fixtures.User(self.sentinel))
        group = self.useFixture(fixtures.Group(self.sentinel))
        self.sentinel.identity.users.add_to_group(user.entity, group.entity)
        self.sentinel.identity.users.remove_from_group(user.entity, group.entity)
        self.assertRaises(
            http.NotFound,
            self.sentinel.identity.users.remove_from_group,
            user.entity,
            group.entity)

    def test_group_has_user(self):
        user = self.useFixture(fixtures.User(self.sentinel))
        group = self.useFixture(fixtures.Group(self.sentinel))
        self.assertRaises(
            http.NotFound,
            self.sentinel.identity.users.check_in_group,
            user.entity,
            group.entity)
        self.sentinel.identity.users.add_to_group(user.entity, group.entity)
        in_group = self.sentinel.identity.users.check_in_group(user.entity, group.entity)
        self.assertEqual(in_group, True)

    def test_group_list_users(self):
        user = self.useFixture(fixtures.User(self.sentinel))
        group = self.useFixture(fixtures.Group(self.sentinel))
        self.sentinel.identity.users.add_to_group(user.entity, group.entity)
        users = self.sentinel.identity.users.list(group=group.entity)
        self.assertThat(user.entity, matchers.IsInCollection(users))

# vi: ts=4 et:

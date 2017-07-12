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

TEST_GROUP = 'sentinel-test'
TEST_GROUP_DESCRIPTION = 'Sentinel Test Group'

SP_TEST_GROUP = 'sentinel-test-sp'

class KeystoneGroupsTestCase(base.KeystoneBaseTestCase):

    def test_create(self):
        group = self.sentinel.groups.create(TEST_GROUP,
                                            description=TEST_GROUP_DESCRIPTION)
        self.addCleanup(self.sentinel.groups.delete, group)
        self.assertEqual(group.name, TEST_GROUP)
        self.assertEqual(group.description, TEST_GROUP_DESCRIPTION)
        self.assertRaises(http.Conflict, self.sentinel.groups.create, TEST_GROUP)

    def test_update(self):
        group = self.sentinel.groups.create(TEST_GROUP)
        self.addCleanup(self.sentinel.groups.delete, group)
        group = self.sentinel.groups.update(group,
                                            description=TEST_GROUP_DESCRIPTION)
        self.assertEqual(group.name, TEST_GROUP)
        self.assertEqual(group.description, TEST_GROUP_DESCRIPTION)

    def test_get(self):
        group = self.sentinel.groups.create(TEST_GROUP)
        self.addCleanup(self.sentinel.groups.delete, group)
        group = self.sentinel.groups.get(group)

    def test_delete(self):
        group = self.sentinel.groups.create(TEST_GROUP)
        self.sentinel.groups.delete(group)
        self.assertRaises(http.NotFound, self.sentinel.groups.delete, group)

    def test_list(self):
        sp_group = self.keystone.groups.create(SP_TEST_GROUP)
        self.addCleanup(self.keystone.groups.delete, sp_group)
        group = self.sentinel.groups.create(TEST_GROUP)
        self.addCleanup(self.sentinel.groups.delete, group)
        groups = self.sentinel.groups.list()
        self.assertThat(group, matchers.IsInCollection(groups))
        self.assertThat(sp_group, matchers.IsNotInCollection(groups))

    def test_group_add_user(self):
        user = self.sentinel.users.create(TEST_GROUP)
        self.addCleanup(self.sentinel.users.delete, user)
        group = self.sentinel.groups.create(TEST_GROUP)
        self.addCleanup(self.sentinel.groups.delete, group)
        self.assertIsNone(self.sentinel.users.add_to_group(user, group))

    def def_group_remove_user(self):
        user = self.sentinel.users.create(TEST_GROUP)
        self.addCleanup(self.sentinel.users.delete, user)
        group = self.sentinel.groups.create(TEST_GROUP)
        self.addCleanup(self.sentinel.groups.delete, group)
        self.assertIsNone(self.sentinel.users.add_to_group(user, group))
        self.sentinel.users.remove_from_group(user, group)
        self.assertRaises(http.NotFound, self.sentinel.users.remove_from_group, user, group)

    def test_group_has_user(self):
        user = self.sentinel.users.create(TEST_GROUP)
        self.addCleanup(self.sentinel.users.delete, user)
        group = self.sentinel.groups.create(TEST_GROUP)
        self.addCleanup(self.sentinel.groups.delete, group)
        self.assertRaises(http.NotFound, self.sentinel.users.check_in_group, user, group)
        self.sentinel.users.add_to_group(user, group)
        self.assertEqual(self.sentinel.users.check_in_group(user, group), True)

    def test_group_list_users(self):
        user = self.sentinel.users.create(TEST_GROUP)
        self.addCleanup(self.sentinel.users.delete, user)
        group = self.sentinel.groups.create(TEST_GROUP)
        self.addCleanup(self.sentinel.groups.delete, group)
        self.sentinel.users.add_to_group(user, group)
        users = self.sentinel.users.list(group=group)
        self.assertThat(user, matchers.IsInCollection(users))

# vi: ts=4 et:

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

TEST_USER = 'test'
TEST_USER_EMAIL = 'test@example.com'
TEST_USER_DESCRIPTION = 'Sentinel Test User'

SP_USER = 'sp_user'

class KeystoneUsersTestCase(base.KeystoneBaseTestCase):

    def test_create(self):
        user = self.sentinel.users.create(TEST_USER,
                                          email=TEST_USER_EMAIL,
                                          description=TEST_USER_DESCRIPTION)
        self.addCleanup(self.sentinel.users.delete, user)
        self.assertEqual(user.name, TEST_USER)
        self.assertEqual(user.email, TEST_USER_EMAIL)
        self.assertEqual(user.description, TEST_USER_DESCRIPTION)
        self.assertEqual(user.enabled, True)
        self.assertRaises(http.Conflict, self.sentinel.users.create, TEST_USER)

    def test_update(self):
        user = self.sentinel.users.create(TEST_USER)
        self.addCleanup(self.sentinel.users.delete, user)
        user = self.sentinel.users.update(user,
                                          email=TEST_USER_EMAIL,
                                          description=TEST_USER_DESCRIPTION,
                                          enabled=False)
        self.assertEqual(user.name, TEST_USER)
        self.assertEqual(user.email, TEST_USER_EMAIL)
        self.assertEqual(user.description, TEST_USER_DESCRIPTION)
        self.assertEqual(user.enabled, False)

    def test_get(self):
        user = self.sentinel.users.create(TEST_USER)
        self.addCleanup(self.sentinel.users.delete, user)
        user = self.sentinel.users.get(user)

    def test_delete(self):
        user = self.sentinel.users.create(TEST_USER)
        self.sentinel.users.delete(user)
        self.assertRaises(http.NotFound, self.sentinel.users.delete, user)

    def test_list(self):
        sp_user = self.keystone.users.create(SP_USER)
        self.addCleanup(self.keystone.users.delete, sp_user)
        user = self.sentinel.users.create(TEST_USER)
        self.addCleanup(self.sentinel.users.delete, user)
        users = self.sentinel.users.list()
        self.assertThat(user, matchers.IsInCollection(users))
        self.assertThat(sp_user, matchers.IsNotInCollection(users))

# vi: ts=4 et:

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

import sentinel.tests.functional.identity.base as base

TEST_USER='test'

class KeystoneUsersTestCase(base.KeystoneBaseTestCase):

    def testCreateDelete(self):
        """Can create and delete new users"""
        user = self.sentinel.users.create(TEST_USER)
        self.addCleanup(self.sentinel.users.delete, user)
        self.assertEqual(user.name, TEST_USER)

    def testUserCreateConflict(self):
        """Cannot redefine users"""
        user = self.sentinel.users.create(TEST_USER)
        self.addCleanup(self.sentinel.users.delete, user)
        self.assertRaises(http.Conflict, self.sentinel.users.create, TEST_USER)

    def testUserDelete(self):
        """Cannot delete non-existant users"""
        user = self.sentinel.users.create(TEST_USER)
        self.sentinel.users.delete(user)
        self.assertRaises(http.NotFound, self.sentinel.users.delete, user)

# vi: ts=4 et:

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

from cinderclient import exceptions

from sentinel.tests.functional import base
from sentinel.tests.functional import client_fixtures as fixtures

TEST_QUOTA = 666
TEST_QUOTA_BODY = {
    'volumes': TEST_QUOTA,
}

class VolumeV2QuotasTestCase(base.BaseTestCase):

    def test_quotas_get(self):
        project = self.useFixture(fixtures.Project(self.sentinel))
        self.sentinel.volume.quotas.get(project.entity.id)

    def test_quotas_get_usage(self):
        project = self.useFixture(fixtures.Project(self.sentinel))
        self.sentinel.volume.quotas.get(project.entity.id, usage=True)

    def test_quotas_get_taint(self):
        project = self.useFixture(fixtures.Project(self.openstack))
        self.assertRaises(
            exceptions.Forbidden,
            self.sentinel.volume.quotas.get,
            project.entity.id)

    def test_quotas_update(self):
        project = self.useFixture(fixtures.Project(self.sentinel))
        quota = self.sentinel.volume.quotas.update(project.entity.id, **TEST_QUOTA_BODY)
        self.assertEqual(quota.volumes, TEST_QUOTA)

    def test_quotas_update_taint(self):
        project = self.useFixture(fixtures.Project(self.openstack))
        self.assertRaises(
            exceptions.Forbidden,
            self.sentinel.volume.quotas.update,
            project.entity.id,
            **TEST_QUOTA_BODY)

    def test_quotas_delete(self):
        project = self.useFixture(fixtures.Project(self.sentinel))
        self.sentinel.volume.quotas.update(project.entity.id, **TEST_QUOTA_BODY)
        self.sentinel.volume.quotas.delete(project.entity.id)

    def test_quotas_delete_taint(self):
        project = self.useFixture(fixtures.Project(self.openstack))
        self.assertRaises(
            exceptions.Forbidden,
            self.sentinel.volume.quotas.delete,
            project.entity.id)

    def test_quotas_get_default(self):
        project = self.useFixture(fixtures.Project(self.sentinel))
        self.sentinel.volume.quotas.defaults(project.entity.id)

    def test_quotas_get_default_taint(self):
        project = self.useFixture(fixtures.Project(self.openstack))
        self.assertRaises(
            exceptions.Forbidden,
            self.sentinel.volume.quotas.defaults,
            project.entity.id)

# vi: ts=4 et:

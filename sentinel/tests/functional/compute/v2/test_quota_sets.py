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

from novaclient import exceptions

from sentinel.tests.functional import base
from sentinel.tests.functional import client_fixtures as fixtures

QUOTA_VALUE = 666


class ComputeV2QuotaSetsTestCase(base.BaseTestCase):

    def test_quota_set_get(self):
        project = self.useFixture(fixtures.Project(self.sentinel))
        self.sentinel.compute.quotas.get(project.entity.id)

    def test_quota_set_get_taint(self):
        project = self.useFixture(fixtures.Project(self.openstack))
        self.assertRaises(
            exceptions.Forbidden,
            self.sentinel.compute.quotas.get,
            project.entity.id)

    def test_quota_set_detail(self):
        project = self.useFixture(fixtures.Project(self.sentinel))
        self.sentinel.compute.quotas.get(project.entity.id, detail=True)

    def test_quota_set_detail_taint(self):
        project = self.useFixture(fixtures.Project(self.openstack))
        self.assertRaises(
            exceptions.Forbidden,
            self.sentinel.compute.quotas.get,
            project.entity.id,
            detail=True)

    def test_quota_set_update(self):
        project = self.useFixture(fixtures.Project(self.sentinel))
        quota = self.sentinel.compute.quotas.update(
            project.entity.id,
            cores=QUOTA_VALUE,
            instances=QUOTA_VALUE,
            ram=QUOTA_VALUE)
        self.assertEqual(quota.cores, QUOTA_VALUE)
        self.assertEqual(quota.instances, QUOTA_VALUE)
        self.assertEqual(quota.ram, QUOTA_VALUE)

    def test_quota_set_update_taint(self):
        project = self.useFixture(fixtures.Project(self.openstack))
        self.assertRaises(
            exceptions.Forbidden,
            self.sentinel.compute.quotas.update,
            project.entity.id,
            cores=QUOTA_VALUE)

    def test_quota_set_delete(self):
        project = self.useFixture(fixtures.Project(self.sentinel))
        self.sentinel.compute.quotas.delete(project.entity.id)

    def test_quota_set_delete_taint(self):
        project = self.useFixture(fixtures.Project(self.openstack))
        self.assertRaises(
            exceptions.Forbidden,
            self.sentinel.compute.quotas.delete,
            project.entity.id)

    def test_quota_set_defaults(self):
        project = self.useFixture(fixtures.Project(self.sentinel))
        self.sentinel.compute.quotas.defaults(project.entity.id)

    def test_quota_set_defaults_taint(self):
        project = self.useFixture(fixtures.Project(self.openstack))
        self.assertRaises(
            exceptions.Forbidden,
            self.sentinel.compute.quotas.defaults,
            project.entity.id)


# vi: ts=4 et:

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

from sentinel.tests.functional import base, matchers
from sentinel.tests.functional import client_fixtures as fixtures


class VolumeV2VolumesTestCase(base.BaseTestCase):

    def test_volume_list(self):
        grant = self.useFixture(fixtures.UserProjectGrant(self.sentinel))
        federated = base.FederatedUserClient(grant.user.entity, grant.project.entity)
        volume1 = self.useFixture(fixtures.Volume(federated))
        volume2 = self.useFixture(fixtures.Volume(federated))
        openstack = base.OpenStackClient()
        volume3 = self.useFixture(fixtures.Volume(openstack))
        # Test filtering
        sentinel = base.SentinelClient()
        volumes = sentinel.volume.volumes.list(search_opts={'all_tenants': 'True'})
        self.assertEqual(len(volumes), 2)
        self.assertThat(volume1.entity, matchers.IsInCollection(volumes))
        self.assertThat(volume2.entity, matchers.IsInCollection(volumes))
        self.assertThat(volume3.entity, matchers.IsNotInCollection(volumes))
        # Test limits
        volumes = sentinel.volume.volumes.list(
            search_opts={'all_tenants': 'True'},
            limit=1)
        self.assertEqual(len(volumes), 1)
        volumes = sentinel.volume.volumes.list(
            search_opts={'all_tenants': 'True'},
            marker=volumes[0].id,
            limit=1)
        self.assertEqual(len(volumes), 1)
        volumes = sentinel.volume.volumes.list(
            search_opts={'all_tenants': 'True'},
            marker=volumes[0].id,
            limit=1)
        self.assertEqual(len(volumes), 0)

# vi: ts=4 et:

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


class NetworkV2FloatingIPsTestCase(base.BaseTestCase):

    def test_floatingip_list(self):
        grant = self.useFixture(fixtures.UserProjectGrant(self.sentinel))
        federated = base.FederatedUserClient(grant.user.entity, grant.project.entity)
        floatingip1 = self.useFixture(fixtures.FloatingIP(federated))
        openstack = base.OpenStackClient()
        floatingip2 = self.useFixture(fixtures.FloatingIP(openstack))
        # Test filtering
        sentinel = base.SentinelClient()
        floatingips = list(sentinel.network.list_floatingips())
        self.assertEqual(len(floatingips), 1)
        self.assertThat(floatingip1.entity, matchers.IsInCollection(floatingips))
        self.assertThat(floatingip2.entity, matchers.IsNotInCollection(floatingips))

# vi: ts=4 et:

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


class ComputeV2ServersTestCase(base.BaseTestCase):

    def test_server_list(self):
        grant = self.useFixture(fixtures.UserProjectGrant(self.sentinel))
        federated = base.FederatedUserClient(grant.user.entity, grant.project.entity)
        server1 = self.useFixture(fixtures.Server(federated))
        server2 = self.useFixture(fixtures.Server(federated))
        openstack = base.OpenStackClient()
        server3 = self.useFixture(fixtures.Server(openstack))
        # Test filtering
        sentinel = base.SentinelClient()
        servers = sentinel.compute.servers.list(search_opts={'all_tenants': 'True'})
        self.assertEqual(len(servers), 2)
        self.assertThat(server1.entity, matchers.IsInCollection(servers))
        self.assertThat(server2.entity, matchers.IsInCollection(servers))
        self.assertThat(server3.entity, matchers.IsNotInCollection(servers))
        # Test limits
        servers = sentinel.compute.servers.list(
            search_opts={'all_tenants': 'True'},
            limit=1)
        self.assertEqual(len(servers), 1)
        servers = sentinel.compute.servers.list(
            search_opts={'all_tenants': 'True'},
            marker=servers[0].id,
            limit=1)
        self.assertEqual(len(servers), 1)
        servers = sentinel.compute.servers.list(
            search_opts={'all_tenants': 'True'},
            marker=servers[0].id,
            limit=1)
        self.assertEqual(len(servers), 0)

# vi: ts=4 et:

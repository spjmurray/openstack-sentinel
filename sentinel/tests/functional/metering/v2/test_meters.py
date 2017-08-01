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

from sentinel.tests.functional import base
from sentinel.tests.functional import client_fixtures as fixtures

COMPUTE_CREATE_START_QUERY = [
    {'field': 'event_type', 'op': 'eq', 'value': 'compute.instance.create.start'}
]

class MeteringV2MetersTestCase(base.BaseTestCase):

    def test_meters_by_type(self):
        grant = self.useFixture(fixtures.UserProjectGrant(self.sentinel))
        client = base.FederatedUserClient(grant.user.entity, grant.project.entity)
        server = self.useFixture(fixtures.Server(client))
        samples = self.sentinel.metering.samples.list(meter_name='vcpus')
        resources = [s.resource_id for s in samples]
        self.assertIn(server.entity.id, resources)

        #events = self.sentinel.metering.events.list(q=COMPUTE_CREATE_START_QUERY)
        #instances = [t['value'] for e in events for t in e['traits'] if t['name'] == 'instance_id']
        #self.assertIn(server.entity.id, instances)

# vi: ts=4 et:

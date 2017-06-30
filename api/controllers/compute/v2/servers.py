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

"""Root controller for /compute/v2/%{tenant_id}/servers"""

import pecan

from sentinel.clients import Clients

class ComputeV2ServersController(object):
    @pecan.expose('json')
    def detail(self):
        domain = pecan.request.context['domain']
        keystone = Clients.keystone(pecan.request.context['conf'])
        projects = keystone.projects.list()
        projects = filter(lambda x: x.domain_id == domain, projects)
        projects = map(lambda x: x.id, projects)

        nova = Clients.nova(pecan.request.context['conf'])
        servers = nova.servers.list(search_opts={'all_tenants': 'True'})
        servers = filter(lambda x: x.tenant_id in projects, servers)

        payload = {
            'servers': map(lambda x: x.to_dict(), servers),
        }

        return payload

# vi: ts=4 et:

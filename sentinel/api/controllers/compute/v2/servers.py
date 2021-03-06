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

"""Root controller for /compute/v2/servers"""

import pecan
import pecan.decorators

from sentinel.api.controllers.base import BaseController
from sentinel.scope import Scope
from sentinel import utils


class ComputeV2ServersController(BaseController):
    """Basic REST controller for server access"""

    service = u'compute'
    collection = u'servers'
    resource = u'server'

    def __init__(self):
        self._custom_actions = {
            'detail': ['GET'],
            'metadata': ['GET'],
        }

    def _scoped_servers(self):
        """Return a detailed list of servers based on scoping requirements"""

        # If project scoped explicitly set the project list
        projects = None if utils.all_projects() else [pecan.request.token.project_id]

        # Must do a detailed search here as it returns the tenant_id field
        servers = self.compute.servers.list(search_opts={'all_tenants': 'True'})

        servers = Scope.filter(servers, projects=projects)
        return utils.paginate(servers, pecan.request.GET.get('marker'),
                              pecan.request.GET.get('limit'))

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    def get_all(self):
        """Return a list of servers scoped to the domain/project"""

        servers = self._scoped_servers()
        servers = [{u'id': x.id, u'name': x.name} for x in servers]
        return self.format_collection(servers)

    @pecan.expose('json')
    def detail(self):
        servers = self._scoped_servers()
        return self.format_collection(servers)

    @pecan.expose('json')
    def metadata(self, server_id):
        """Return metadata associated with an instance"""

        server = self.compute.servers.get(server_id)

        if server.tenant_id not in Scope.projects():
            pecan.abort(403, 'unauthorized access a resource outside of your domain')

        # Required by Fog, but oddly not in novaclient.v2.servers
        return {u'metadata': server.metadata}


# vi: ts=4 et:

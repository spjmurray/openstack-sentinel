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

import oslo_utils.strutils
import pecan
import pecan.decorators

from sentinel.api.controllers.base import BaseController
from sentinel.scope import Scope


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

    def _all_projects(self):
        """Do we want all projects in out domain"""

        # A basic copy of nova API
        all_projects = pecan.request.GET.get('all_tenants')
        if all_projects:
            return oslo_utils.strutils.bool_from_string(all_projects, True)

        # An empty string is considered consent
        return 'all_tenants' in pecan.request.GET

    def _scoped_servers(self):
        """Return a detailed list of servers based on scoping requirements"""

        # If the client requested all projects return those within the
        # domain scope, same applies for a domain scoped token, otherwise
        # scope to the specifc project
        if self._all_projects() or not pecan.request.token.project_id:
            projects = Scope.projects()
        else:
            projects = [pecan.request.token.project_id]

        # Must do a detailed search here as it returns the tenant_id field
        servers = self.compute.servers.list(search_opts={'all_tenants': 'True'})

        # Filter out only servers within the IdP domain scope
        return [x for x in servers if x.tenant_id in projects]

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

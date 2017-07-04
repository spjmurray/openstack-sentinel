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

import oslo_utils.strutils
import pecan
import pecan.decorators
import pecan.rest

from sentinel.clients import Clients
from sentinel.whitelist import Whitelist


def _all_projects():
    """Do we want all projects in out domain"""

    # A basic copy of nova API
    all_projects = pecan.request.GET.get('all_tenants')
    if all_projects:
        return oslo_utils.strutils.bool_from_string(all_projects, True)

    # An empty string is considered consent
    return 'all_tenants' in pecan.request.GET


def _scoped_projects():
    """Return a list of projects within our domain scope"""

    domain = pecan.request.context['domain']
    keystone = Clients.keystone(pecan.request.context['conf'])
    projects = keystone.projects.list()

    # Assumes that domains cannot be nested
    projects = filter(lambda x: x.domain_id == domain, projects)
    return map(lambda x: x.id, projects)


def _scoped_servers():
    """Return a detailed list of servers based on scoping requirements"""

    # If the client requested all projects return those within the
    # domain scope, else just that indicated by the token binding
    if _all_projects():
        projects = _scoped_projects()
    else:
        projects = [pecan.request.context['token'].project_id]

    # Must do a detailed search here as it returns the tenant_id field
    nova = Clients.nova(pecan.request.context['conf'])
    servers = nova.servers.list(search_opts={'all_tenants': 'True'})

    # Filter out only servers within the IdP domain scope
    return filter(lambda x: x.tenant_id in projects, servers)


class ComputeV2ServersController(pecan.rest.RestController):
    """Basic REST controller for server access"""

    def __init__(self):
        self._custom_actions = {
            'detail': ['GET'],
        }

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    def get_all(self):
        """Return a list of servers scoped to the domain/project"""

        servers = _scoped_servers()
        payload = {
            u'servers': map(lambda x: { u'id': x.id, u'name': x.name }, servers),
        }

        return payload

    @pecan.expose('json')
    def detail(self):
        """Return a detailed list of servers scoped to the domain/project"""

        payload = {
            u'servers': Whitelist.apply(_scoped_servers()),
        }

        return payload

# vi: ts=4 et:

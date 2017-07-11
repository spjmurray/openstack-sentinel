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

"""Controller for /identity/v3/projects"""

import logging

import pecan
import pecan.decorators
import pecan.rest

from sentinel.clients import Clients
from sentinel.whitelist import Whitelist

LOG = logging.getLogger(__name__)


class IdentityV3ProjectsController(pecan.rest.RestController):
    """Controller for the projects collection"""

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    def get_all(self):
        """List all projects in the IdP domain"""

        keystone = Clients.keystone()

        projects = keystone.projects.list(domain=pecan.request.context['domain'])

        payload = {
            u'links': {
                u'next': None,
                u'previous': None,
                u'self': pecan.request.path_url,
            },
            u'projects': Whitelist.apply(projects),
        }

        return payload

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    def post(self):
        """Create a new project in the IdP domain"""

        keystone = Clients.keystone()

        # Hard code the IdP domain ID
        project = keystone.projects.create(pecan.request.json['project'].get('name'),
                                           pecan.request.context['domain'],
                                           description=pecan.request.json['project'].get('description'),
                                           enabled=pecan.request.json['project'].get('enabled'),
                                           parent=pecan.request.json['project'].get('parent_id'))

        LOG.info('client %s created project %s', pecan.request.context['user'], project.id)

        payload = {
            u'project': Whitelist.apply(project),
        }

        pecan.response.status = 201
        return payload

    @pecan.expose('json')
    def get(self, project_id):
        """Get a specific project from the IdP domain"""

        keystone = Clients.keystone()

        query = pecan.request.GET
        params = ['subtree_as_list', 'subtree_as_ids', 'parents_as_list', 'parents_as_ids']
        kwargs = {x: True for x in params if x in query}

        project = keystone.projects.get(project_id, **kwargs)

        if project.domain_id != pecan.request.context['domain']:
            pecan.abort(403, 'unauthorized access a resource outside of your domain')

        payload = {
            u'project': Whitelist.apply(project),
        }

        return payload

    @pecan.expose('json')
    def patch(self, project_id):
        """Update a specific project in the IdP domain"""

        keystone = Clients.keystone()

        project = keystone.projects.get(project_id)

        if project.domain_id != pecan.request.context['domain']:
            pecan.abort(403, 'unauthorized access a resource outside of your domain')

        project = keystone.projects.update(project,
                                           name=pecan.request.json['project'].get('name'),
                                           description=pecan.request.json['project'].get('description'),
                                           enabled=pecan.request.json['project'].get('enabled'))

        payload = {
            u'project': Whitelist.apply(project),
        }

        return payload

    @pecan.expose('json')
    def delete(self, project_id):
        """Delete a specific project from the IdP domain"""

        keystone = Clients.keystone()

        project = keystone.projects.get(project_id)

        if project.domain_id != pecan.request.context['domain']:
            pecan.abort(403, 'unauthorized access a resource outside of your domain')

        keystone.projects.delete(project)

        LOG.info('client %s deleted user %s', pecan.request.context['user'], project.id)

        pecan.response.status = 204

# vi: ts=4 et:

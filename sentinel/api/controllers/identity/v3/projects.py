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

import pecan
import pecan.decorators
import pecan.rest

from sentinel import utils
from sentinel.clients import Clients
from sentinel.whitelist import Whitelist


class IdentityV3ProjectsController(pecan.rest.RestController):
    """Controller for the projects collection"""

    collection = u'projects'
    resource = u'project'

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    def get_all(self):
        keystone = Clients.keystone()
        projects = keystone.projects.list(
            domain=pecan.request.context['domain'])
        return utils.render_with_links(self.collection, Whitelist.apply(projects))

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    def post(self):
        keystone = Clients.keystone()
        project = keystone.projects.create(
            pecan.request.json['project'].get('name'),
            pecan.request.context['domain'],
            description=pecan.request.json['project'].get('description'),
            enabled=pecan.request.json['project'].get('enabled'),
            parent=pecan.request.json['project'].get('parent_id'))
        pecan.response.status = 201
        return utils.render(self.resource, Whitelist.apply(project))

    @pecan.expose('json')
    def get(self, project_id):
        keystone = Clients.keystone()
        query = pecan.request.GET
        params = ['subtree_as_list', 'subtree_as_ids', 'parents_as_list', 'parents_as_ids']
        kwargs = {x: True for x in params if x in query}
        project = keystone.projects.get(project_id, **kwargs)
        utils.check_permissions(project)
        return utils.render(self.resource, Whitelist.apply(project))

    @pecan.expose('json')
    def patch(self, project_id):
        keystone = Clients.keystone()
        project = keystone.projects.get(project_id)
        utils.check_permissions(project)
        project = keystone.projects.update(
            project,
            name=pecan.request.json['project'].get('name'),
            description=pecan.request.json['project'].get('description'),
            enabled=pecan.request.json['project'].get('enabled'))
        return utils.render(self.resource, Whitelist.apply(project))

    @pecan.expose('json')
    def delete(self, project_id):
        keystone = Clients.keystone()
        project = keystone.projects.get(project_id)
        utils.check_permissions(project)
        keystone.projects.delete(project)
        pecan.response.status = 204

# vi: ts=4 et:

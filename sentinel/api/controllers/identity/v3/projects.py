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

from sentinel import utils
from sentinel.api.controllers.base import BaseController
from sentinel.clients import Clients


class IdentityV3ProjectsUsersRolesController(BaseController):
    """Controller for project-user roles"""

    collection = u'roles'
    resource = u'role'

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    def get_all(self, project_id, user_id):
        keystone = Clients.keystone()
        project = keystone.projects.get(project_id)
        user = keystone.users.get(user_id)
        roles = keystone.roles.list(user=user, project=project)
        return self.format_collection(roles)

    @pecan.expose('json')
    def put(self, project_id, user_id, role_id):
        keystone = Clients.keystone()
        project = keystone.projects.get(project_id)
        user = keystone.users.get(user_id)
        role = keystone.roles.get(role_id)
        keystone.roles.grant(role, user=user, project=project)
        pecan.response.status = 204

    @pecan.expose('json')
    def head(self, project_id, user_id, role_id):
        keystone = Clients.keystone()
        project = keystone.projects.get(project_id)
        user = keystone.users.get(user_id)
        role = keystone.roles.get(role_id)
        keystone.roles.check(role, user=user, project=project)
        pecan.response.status = 204

    @pecan.expose('json')
    def delete(self, project_id, user_id, role_id):
        keystone = Clients.keystone()
        project = keystone.projects.get(project_id)
        user = keystone.users.get(user_id)
        role = keystone.roles.get(role_id)
        keystone.roles.revoke(role, user=user, project=project)
        pecan.response.status = 204


class IdentityV3ProjectsUsersController(BaseController):

    def __init__(self):
        self.roles = IdentityV3ProjectsUsersRolesController()

    def get(self, project_id, user_id):
        # Required for routing
        pecan.response.status = 404


class IdentityV3ProjectsGroupsRolesController(BaseController):
    """Controller for project-group roles"""

    collection = u'roles'
    resource = u'role'

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    def get_all(self, project_id, group_id):
        keystone = Clients.keystone()
        project = keystone.projects.get(project_id)
        group = keystone.groups.get(group_id)
        roles = keystone.roles.list(group=group, project=project)
        return self.format_collection(roles)

    @pecan.expose('json')
    def put(self, project_id, group_id, role_id):
        keystone = Clients.keystone()
        project = keystone.projects.get(project_id)
        group = keystone.groups.get(group_id)
        role = keystone.roles.get(role_id)
        keystone.roles.grant(role, group=group, project=project)
        pecan.response.status = 204

    @pecan.expose('json')
    def head(self, project_id, group_id, role_id):
        keystone = Clients.keystone()
        project = keystone.projects.get(project_id)
        group = keystone.groups.get(group_id)
        role = keystone.roles.get(role_id)
        keystone.roles.check(role, group=group, project=project)
        pecan.response.status = 204

    @pecan.expose('json')
    def delete(self, project_id, group_id, role_id):
        keystone = Clients.keystone()
        project = keystone.projects.get(project_id)
        group = keystone.groups.get(group_id)
        role = keystone.roles.get(role_id)
        keystone.roles.revoke(role, group=group, project=project)
        pecan.response.status = 204


class IdentityV3ProjectsGroupsController(BaseController):

    def __init__(self):
        self.roles = IdentityV3ProjectsGroupsRolesController()

    def get(self, project_id, group_id):
        # Required for routing
        pecan.response.status = 404


class IdentityV3ProjectsController(BaseController):
    """Controller for the projects collection"""

    collection = u'projects'
    resource = u'project'

    def __init__(self):
        self.groups = IdentityV3ProjectsGroupsController()
        self.users = IdentityV3ProjectsUsersController()

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    def get_all(self):
        keystone = Clients.keystone()
        projects = keystone.projects.list(
            domain=pecan.request.context['domain'])
        return self.format_collection(projects)

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
        return self.format_resource(project)

    @pecan.expose('json')
    def get(self, project_id):
        keystone = Clients.keystone()
        query = pecan.request.GET
        params = ['subtree_as_list', 'subtree_as_ids', 'parents_as_list', 'parents_as_ids']
        kwargs = {x: True for x in params if x in query}
        project = keystone.projects.get(project_id, **kwargs)
        utils.check_permissions(project)
        return self.format_resource(project)

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
        return self.format_resource(project)

    @pecan.expose('json')
    def delete(self, project_id):
        keystone = Clients.keystone()
        project = keystone.projects.get(project_id)
        utils.check_permissions(project)
        keystone.projects.delete(project)
        pecan.response.status = 204

# vi: ts=4 et:

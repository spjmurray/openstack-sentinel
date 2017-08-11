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

from sentinel.api.controllers.base import BaseController
from sentinel.decorators import supported_queries, mutate_arguments


class IdentityV3ProjectsUsersRolesController(BaseController):
    """Controller for project-user roles"""

    service = u'identity'
    collection = u'roles'
    resource = u'role'

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    @mutate_arguments('identity.projects', 'identity.users')
    def get_all(self, project, user):
        roles = self.identity.roles.list(user=user, project=project)
        return self.format_collection(roles)

    @pecan.expose('json')
    @mutate_arguments('identity.projects', 'identity.users', 'identity.roles')
    def put(self, project, user, role):
        self.identity.roles.grant(role, user=user, project=project)
        pecan.response.status = 204

    @pecan.expose('json')
    @mutate_arguments('identity.projects', 'identity.users', 'identity.roles')
    def head(self, project, user, role):
        self.identity.roles.check(role, user=user, project=project)
        pecan.response.status = 204

    @pecan.expose('json')
    @mutate_arguments('identity.projects', 'identity.users', 'identity.roles')
    def delete(self, project, user, role):
        self.identity.roles.revoke(role, user=user, project=project)
        pecan.response.status = 204


class IdentityV3ProjectsUsersController(BaseController):

    def __init__(self):
        self.roles = IdentityV3ProjectsUsersRolesController()

    # pylint: disable=unused-argument
    def get(self, project_id, user_id):
        # Required for routing
        pecan.response.status = 404


class IdentityV3ProjectsGroupsRolesController(BaseController):
    """Controller for project-group roles"""

    service = u'identity'
    collection = u'roles'
    resource = u'role'

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    @mutate_arguments('identity.projects', 'identity.groups')
    def get_all(self, project, group):
        roles = self.identity.roles.list(group=group, project=project)
        return self.format_collection(roles)

    @pecan.expose('json')
    @mutate_arguments('identity.projects', 'identity.groups', 'identity.roles')
    def put(self, project, group, role):
        self.identity.roles.grant(role, group=group, project=project)
        pecan.response.status = 204

    @pecan.expose('json')
    @mutate_arguments('identity.projects', 'identity.groups', 'identity.roles')
    def head(self, project, group, role):
        self.identity.roles.check(role, group=group, project=project)
        pecan.response.status = 204

    @pecan.expose('json')
    @mutate_arguments('identity.projects', 'identity.groups', 'identity.roles')
    def delete(self, project, group, role):
        self.identity.roles.revoke(role, group=group, project=project)
        pecan.response.status = 204


class IdentityV3ProjectsGroupsController(BaseController):

    def __init__(self):
        self.roles = IdentityV3ProjectsGroupsRolesController()

    # pylint: disable=unused-argument
    def get(self, project_id, group_id):
        # Required for routing
        pecan.response.status = 404


class IdentityV3ProjectsController(BaseController):
    """Controller for the projects collection"""

    service = u'identity'
    collection = u'projects'
    resource = u'project'

    def __init__(self):
        self.groups = IdentityV3ProjectsGroupsController()
        self.users = IdentityV3ProjectsUsersController()

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    @supported_queries()
    def get_all(self):
        projects = self.identity.projects.list(
            domain=pecan.request.domain_id)
        return self.format_collection(projects)

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    def post(self):
        project = self.identity.projects.create(
            pecan.request.json['project'].get('name'),
            pecan.request.domain_id,
            description=pecan.request.json['project'].get('description'),
            enabled=pecan.request.json['project'].get('enabled'),
            parent=pecan.request.json['project'].get('parent_id'))
        pecan.response.status = 201
        return self.format_resource(project)

    @pecan.expose('json')
    @supported_queries('subtree_as_list', 'subtree_as_ids', 'parents_as_list', 'parents_as_ids')
    @mutate_arguments('identity.projects')
    def get(self, project):
        kwargs = {x: True for x in pecan.request.GET}
        project = self.identity.projects.get(project, **kwargs)
        return self.format_resource(project)

    @pecan.expose('json')
    @mutate_arguments('identity.projects')
    def patch(self, project):
        project = self.identity.projects.update(
            project,
            name=pecan.request.json['project'].get('name'),
            description=pecan.request.json['project'].get('description'),
            enabled=pecan.request.json['project'].get('enabled'))
        return self.format_resource(project)

    @pecan.expose('json')
    @mutate_arguments('identity.projects')
    def delete(self, project):
        self.identity.projects.delete(project)
        pecan.response.status = 204

# vi: ts=4 et:

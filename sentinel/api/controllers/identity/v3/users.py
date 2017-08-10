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

"""Controller for /identity/v3/users"""

import pecan
import pecan.decorators

from sentinel.api.controllers.base import BaseController
from sentinel.decorators import supported_queries, mutate_arguments


class IdentityV3UsersController(BaseController):
    """Controller for the users collection"""

    collection = u'users'
    resource = u'user'

    def __init__(self):
        self._custom_actions = {
            'groups': ['GET'],
            'projects': ['GET'],
        }

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    @supported_queries()
    def get_all(self):
        users = self.identity.users.list(
            domain=pecan.request.domain_id)
        return self.format_collection(users)

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    def post(self):
        user = self.identity.users.create(
            pecan.request.json['user']['name'],
            domain=pecan.request.domain_id,
            password=pecan.request.json['user'].get('password'), # Required for testing
            email=pecan.request.json['user'].get('email'),
            description=pecan.request.json['user'].get('description'),
            enabled=pecan.request.json['user'].get('enabled'))
        pecan.response.status = 201
        return self.format_resource(user)

    @pecan.expose('json')
    @mutate_arguments('identity.users')
    def get(self, user):
        return self.format_resource(user)

    @pecan.expose('json')
    @mutate_arguments('identity.users')
    def patch(self, user):
        user = self.identity.users.update(
            user,
            name=pecan.request.json['user'].get('name'),
            email=pecan.request.json['user'].get('email'),
            description=pecan.request.json['user'].get('description'),
            enabled=pecan.request.json['user'].get('enabled'))
        return self.format_resource(user)

    @pecan.expose('json')
    @mutate_arguments('identity.users')
    def delete(self, user):
        self.identity.users.delete(user)
        pecan.response.status = 204

    @pecan.expose('json')
    @mutate_arguments('identity.users')
    def groups(self, user):
        groups = self.identity.groups.list(user=user, domain=pecan.request.domain_id)
        return self.format_collection(groups, resource=u'group', collection=u'groups')

    @pecan.expose('json')
    @mutate_arguments('identity.users')
    def projects(self, user):
        projects = self.identity.projects.list(user=user, domain=pecan.request.domain_id)
        return self.format_collection(projects, resource=u'project', collection=u'projects')

# vi: ts=4 et:

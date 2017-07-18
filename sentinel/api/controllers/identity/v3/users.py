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

from sentinel import utils
from sentinel.api.controllers.base import BaseController
from sentinel.clients import Clients


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
    def get_all(self):
        keystone = Clients.keystone()
        users = keystone.users.list(
            domain=pecan.request.context['domain'])
        return self.format_collection(users)

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    def post(self):
        keystone = Clients.keystone()
        user = keystone.users.create(
            pecan.request.json['user']['name'],
            domain=pecan.request.context['domain'],
            email=pecan.request.json['user'].get('email'),
            description=pecan.request.json['user'].get('description'),
            enabled=pecan.request.json['user'].get('enabled'))
        pecan.response.status = 201
        return self.format_resource(user)

    @pecan.expose('json')
    def get(self, user_id):
        keystone = Clients.keystone()
        user = keystone.users.get(user_id)
        utils.check_permissions(user)
        return self.format_resource(user)

    @pecan.expose('json')
    def patch(self, user_id):
        keystone = Clients.keystone()
        user = keystone.users.get(user_id)
        utils.check_permissions(user)
        user = keystone.users.update(
            user,
            name=pecan.request.json['user'].get('name'),
            email=pecan.request.json['user'].get('email'),
            description=pecan.request.json['user'].get('description'),
            enabled=pecan.request.json['user'].get('enabled'))
        return self.format_resource(user)

    @pecan.expose('json')
    def delete(self, user_id):
        keystone = Clients.keystone()
        user = keystone.users.get(user_id)
        utils.check_permissions(user)
        keystone.users.delete(user)
        pecan.response.status = 204

    @pecan.expose('json')
    def groups(self, user_id):
        keystone = Clients.keystone()
        user = keystone.users.get(user_id)
        utils.check_permissions(user)
        groups = keystone.groups.list(user=user, domain=pecan.request.context['domain'])
        return self.format_collection(groups, resource=u'group', collection=u'groups')

    @pecan.expose('json')
    def projects(self, user_id):
        keystone = Clients.keystone()
        user = keystone.users.get(user_id)
        utils.check_permissions(user)
        projects = keystone.projects.list(user=user, domain=pecan.request.context['domain'])
        return self.format_collection(projects, resource=u'project', collection=u'projects')

# vi: ts=4 et:

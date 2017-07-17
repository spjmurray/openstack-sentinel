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
import pecan.rest

from sentinel import utils
from sentinel.clients import Clients
from sentinel.whitelist import Whitelist


class IdentityV3UsersController(pecan.rest.RestController):
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
        return utils.render_with_links(self.collection, Whitelist.apply(users))

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
        return utils.render(self.resource, Whitelist.apply(user))

    @pecan.expose('json')
    def get(self, user_id):
        keystone = Clients.keystone()
        user = keystone.users.get(user_id)
        utils.check_permissions(user)
        return utils.render(self.resource, Whitelist.apply(user))

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
        return utils.render(self.resource, Whitelist.apply(user))

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
        return utils.render_with_links(u'groups', Whitelist.apply(groups, 'sentinel.api.controllers.identity.v3.groups'))

    @pecan.expose('json')
    def projects(self, user_id):
        keystone = Clients.keystone()
        user = keystone.users.get(user_id)
        utils.check_permissions(user)
        projects = keystone.projects.list(user=user, domain=pecan.request.context['domain'])
        return utils.render_with_links(u'projects', Whitelist.apply(projects, 'sentinel.api.controllers.identity.v3.projects'))

# vi: ts=4 et:

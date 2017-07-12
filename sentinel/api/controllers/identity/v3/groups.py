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

"""Controller for /identity/v3/groups"""

import pecan
import pecan.decorators
import pecan.rest

from sentinel import utils
from sentinel.clients import Clients
from sentinel.whitelist import Whitelist


class IdentityV3GroupsUsersController(pecan.rest.RestController):
    """Controller for interacting with group users"""

    @pecan.expose('json')
    def get(self, group_id):
        keystone = Clients.keystone()
        group = keystone.groups.get(group_id)
        utils.check_permissions(group)
        users = keystone.users.list(group=group)
        return utils.render_with_links(
            u'users',
            Whitelist.apply(users, 'sentinel.api.controllers.identity.v3.users'))

    @pecan.expose('json')
    def put(self, group_id, user_id):
        keystone = Clients.keystone()
        user = keystone.users.get(user_id)
        group = keystone.groups.get(group_id)
        utils.check_permissions(user, group)
        keystone.users.add_to_group(user, group)
        pecan.response.status = 204

    @pecan.expose('json')
    def head(self, group_id, user_id):
        keystone = Clients.keystone()
        user = keystone.users.get(user_id)
        group = keystone.groups.get(group_id)
        utils.check_permissions(user, group)
        keystone.users.check_in_group(user, group)
        pecan.response.status = 204

    @pecan.expose('json')
    def delete(self, group_id, user_id):
        keystone = Clients.keystone()
        user = keystone.users.get(user_id)
        group = keystone.groups.get(group_id)
        utils.check_permissions(user, group)
        keystone.users.remove_from_group(user, group)
        pecan.response.status = 204


class IdentityV3GroupsController(pecan.rest.RestController):
    """Controller for the groups collection"""

    collection = u'groups'
    resource = u'group'

    def __init__(self):
        self.users = IdentityV3GroupsUsersController()

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    def get_all(self):
        keystone = Clients.keystone()
        groups = keystone.groups.list(
            domain=pecan.request.context['domain'])
        return utils.render_with_links(self.collection, Whitelist.apply(groups))

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    def post(self):
        keystone = Clients.keystone()
        group = keystone.groups.create(
            pecan.request.json['group'].get('name'),
            pecan.request.context['domain'],
            description=pecan.request.json['group'].get('description'))
        pecan.response.status = 201
        return utils.render(self.resource, Whitelist.apply(group))

    @pecan.expose('json')
    def get(self, group_id):
        keystone = Clients.keystone()
        group = keystone.groups.get(group_id)
        utils.check_permissions(group)
        return utils.render(self.resource, Whitelist.apply(group))

    @pecan.expose('json')
    def patch(self, group_id):
        keystone = Clients.keystone()
        group = keystone.groups.get(group_id)
        utils.check_permissions(group)
        group = keystone.groups.update(
            group,
            name=pecan.request.json['group'].get('name'),
            description=pecan.request.json['group'].get('description'))
        return utils.render(self.resource, Whitelist.apply(group))

    @pecan.expose('json')
    def delete(self, group_id):
        keystone = Clients.keystone()
        group = keystone.groups.get(group_id)
        utils.check_permissions(group)
        keystone.groups.delete(group)
        pecan.response.status = 204

# vi: ts=4 et:

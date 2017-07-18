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

from sentinel import utils
from sentinel.api.controllers.base import BaseController


class IdentityV3GroupsUsersController(BaseController):
    """Controller for interacting with group users"""

    collection = u'users'
    resource = u'user'

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    def get_all(self, group_id):
        group = self.identity.groups.get(group_id)
        utils.check_permissions(group)
        users = self.identity.users.list(group=group)
        return self.format_collection(users)

    @pecan.expose('json')
    def put(self, group_id, user_id):
        user = self.identity.users.get(user_id)
        group = self.identity.groups.get(group_id)
        utils.check_permissions(user, group)
        self.identity.users.add_to_group(user, group)
        pecan.response.status = 204

    @pecan.expose('json')
    def head(self, group_id, user_id):
        user = self.identity.users.get(user_id)
        group = self.identity.groups.get(group_id)
        utils.check_permissions(user, group)
        self.identity.users.check_in_group(user, group)
        pecan.response.status = 204

    @pecan.expose('json')
    def delete(self, group_id, user_id):
        user = self.identity.users.get(user_id)
        group = self.identity.groups.get(group_id)
        utils.check_permissions(user, group)
        self.identity.users.remove_from_group(user, group)
        pecan.response.status = 204


class IdentityV3GroupsController(BaseController):
    """Controller for the groups collection"""

    collection = u'groups'
    resource = u'group'

    def __init__(self):
        self.users = IdentityV3GroupsUsersController()

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    def get_all(self):
        groups = self.identity.groups.list(
            domain=pecan.request.context['domain'])
        return self.format_collection(groups)

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    def post(self):
        group = self.identity.groups.create(
            pecan.request.json['group'].get('name'),
            pecan.request.context['domain'],
            description=pecan.request.json['group'].get('description'))
        pecan.response.status = 201
        return self.format_resource(group)

    @pecan.expose('json')
    def get(self, group_id):
        group = self.identity.groups.get(group_id)
        utils.check_permissions(group)
        return self.format_resource(group)

    @pecan.expose('json')
    def patch(self, group_id):
        group = self.identity.groups.get(group_id)
        utils.check_permissions(group)
        group = self.identity.groups.update(
            group,
            name=pecan.request.json['group'].get('name'),
            description=pecan.request.json['group'].get('description'))
        return self.format_resource(group)

    @pecan.expose('json')
    def delete(self, group_id):
        group = self.identity.groups.get(group_id)
        utils.check_permissions(group)
        self.identity.groups.delete(group)
        pecan.response.status = 204

# vi: ts=4 et:

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

from sentinel.api.controllers.base import BaseController
from sentinel.decorators import supported_queries, mutate_arguments


class IdentityV3GroupsUsersController(BaseController):
    """Controller for interacting with group users"""

    collection = u'users'
    resource = u'user'

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    @supported_queries()
    @mutate_arguments('identity.groups')
    def get_all(self, group):
        users = self.identity.users.list(group=group)
        return self.format_collection(users)

    @pecan.expose('json')
    @mutate_arguments('identity.groups', 'identity.users')
    def put(self, group, user):
        self.identity.users.add_to_group(user, group)
        pecan.response.status = 204

    @pecan.expose('json')
    @mutate_arguments('identity.groups', 'identity.users')
    def head(self, group, user):
        self.identity.users.check_in_group(user, group)
        pecan.response.status = 204

    @pecan.expose('json')
    @mutate_arguments('identity.groups', 'identity.users')
    def delete(self, group, user):
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
    @supported_queries()
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
    @mutate_arguments('identity.groups')
    def get(self, group):
        return self.format_resource(group)

    @pecan.expose('json')
    @mutate_arguments('identity.groups')
    def patch(self, group):
        group = self.identity.groups.update(
            group,
            name=pecan.request.json['group'].get('name'),
            description=pecan.request.json['group'].get('description'))
        return self.format_resource(group)

    @pecan.expose('json')
    @mutate_arguments('identity.groups')
    def delete(self, group):
        self.identity.groups.delete(group)
        pecan.response.status = 204

# vi: ts=4 et:

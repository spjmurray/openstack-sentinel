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

import keystoneauth1.exceptions
import logging
import pecan
import pecan.decorators
import pecan.rest

from sentinel.whitelist import Whitelist
from sentinel.clients import Clients

LOG = logging.getLogger(__name__)


class IdentityV3UsersController(pecan.rest.RestController):
    """Controller for the users collection"""

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    def get_all(self):
        """Return a list of all users in the IdP domain"""

        keystone = Clients.keystone(pecan.request.context['conf'])
        users = keystone.users.list(domain=pecan.request.context['domain'])

        payload = {
            u'links': {
                u'next': None,
                u'previous': None,
                u'self': pecan.request.application_url,
            },
            u'users': Whitelist.apply(users),
        }

        return payload

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    def post(self):
        """Create a new user in the IdP domain"""

        keystone = Clients.keystone(pecan.request.context['conf'])

        # Hard code the user domain for the IdP
        try:
            user = keystone.users.create(pecan.request.json['user']['name'],
                domain=pecan.request.context['domain'],
                enabled=True)
        except keystoneauth1.exceptions.HttpError as e:
            pecan.abort(e.http_status, e.message)

        LOG.info('client domain {} created new user {}'.format(
            pecan.request.context['domain'], user.id))

        payload = {
            u'user': Whitelist.apply(user),
        }

        pecan.response.status = 201
        return payload

    @pecan.expose('json')
    def get_one(self, user_id):
        """Return the specified user"""

        keystone = Clients.keystone(pecan.request.context['conf'])
        user = keystone.users.get(user_id)

        # Check the IdP is allowed to access this resource
        if user.domain_id != pecan.request.context['domain']:
            LOG.warn('client domain {} not permitted to access user {}'.format(
                pecan.request.context['domain'], user.id))
            pecan.abort(403)

        payload = {
            u'user': Whitelist.apply(user),
        }

        return payload

    @pecan.expose('json')
    def delete(self, user_id):
        """Delete the specified user"""

        keystone = Clients.keystone(pecan.request.context['conf'])
        user = keystone.users.get(user_id)

        # Check the IdP is allowed to access this resource
        if user.domain_id != pecan.request.context['domain']:
            LOG.warn('client domain {} not permitted to delete user {}'.format(
                pecan.request.context['domain'], user.id))
            pecan.abort(403)

        keystone.users.delete(user)

        LOG.info('client domain {} deleted user {}'.format(
            pecan.request.context['domain'], user.id))

        pecan.response.status = 204


# vi: ts=4 et:

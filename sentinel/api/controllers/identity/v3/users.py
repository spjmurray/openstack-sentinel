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

import logging

import pecan
import pecan.decorators
import pecan.rest

from sentinel.clients import Clients
from sentinel.whitelist import Whitelist

LOG = logging.getLogger(__name__)


class IdentityV3UsersController(pecan.rest.RestController):
    """Controller for the users collection"""

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    def get_all(self):
        """Return a list of all users in the IdP domain"""

        keystone = Clients.keystone()

        users = keystone.users.list(domain=pecan.request.context['domain'])

        payload = {
            u'links': {
                u'next': None,
                u'previous': None,
                u'self': pecan.request.path_url,
            },
            u'users': Whitelist.apply(users),
        }

        return payload

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    def post(self):
        """Create a new user in the IdP domain"""

        keystone = Clients.keystone()

        # Hard code the user domain for the IdP
        user = keystone.users.create(pecan.request.json['user']['name'],
                                     domain=pecan.request.context['domain'],
                                     email=pecan.request.json['user'].get('email'),
                                     description=pecan.request.json['user'].get('description'),
                                     enabled=pecan.request.json['user'].get('enabled'))

        LOG.info('client %s created user %s', pecan.request.context['user'], user.id)

        payload = {
            u'user': Whitelist.apply(user),
        }

        pecan.response.status = 201
        return payload

    @pecan.expose('json')
    def patch(self, user_id):
        """Update a user in the IdP domain"""

        keystone = Clients.keystone()

        user = keystone.users.get(user_id)

        if user.domain_id != pecan.request.context['domain']:
            pecan.abort(403, 'unauthorized access a resource outside of your domain')

        # Deny the changing of domain, you could escape from the federated zone
        user = keystone.users.update(user,
                                     name=pecan.request.json['user'].get('name'),
                                     email=pecan.request.json['user'].get('email'),
                                     description=pecan.request.json['user'].get('description'),
                                     enabled=pecan.request.json['user'].get('enabled'))

        payload = {
            u'user': Whitelist.apply(user),
        }

        return payload

    @pecan.expose('json')
    def get_one(self, user_id):
        """Return the specified user"""

        keystone = Clients.keystone()

        user = keystone.users.get(user_id)

        # Check the IdP is allowed to access this resource
        if user.domain_id != pecan.request.context['domain']:
            pecan.abort(403, 'unauthorized access a resource outside of your domain')

        payload = {
            u'user': Whitelist.apply(user),
        }

        return payload

    @pecan.expose('json')
    def delete(self, user_id):
        """Delete the specified user"""

        keystone = Clients.keystone()

        user = keystone.users.get(user_id)

        # Check the IdP is allowed to access this resource
        if user.domain_id != pecan.request.context['domain']:
            pecan.abort(403, 'unauthorized access a resource outside of your domain')

        keystone.users.delete(user)

        LOG.info('client %s deleted user %s', pecan.request.context['user'], user.id)

        pecan.response.status = 204


# vi: ts=4 et:

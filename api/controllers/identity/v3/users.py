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

from sentinel.whitelist import Whitelist
from sentinel.clients import Clients

class IdentityV3UsersController(object):

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    def index(self):
        keystone = Clients.keystone(pecan.request.context['conf'])
        users = keystone.users.list(domain=pecan.request.context['domain'])

        payload = {
            'links': {
                'next': None,
                'previous': None,
                'self': pecan.request.application_url,
            },
            'users': Whitelist.apply(users),
        }

        return payload

# vi: ts=4 et:

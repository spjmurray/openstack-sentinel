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

"""Controller for /identity/v3/roles"""

import pecan
import pecan.decorators
import pecan.rest

from sentinel import utils
from sentinel.clients import Clients
from sentinel.whitelist import Whitelist

class IdentityV3RolesController(pecan.rest.RestController):
    """Controller for the roles collection"""

    collection = u'roles'
    resource = u'role'

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    def get_all(self):
        keystone = Clients.keystone()
        roles = keystone.roles.list(
            domain_id=pecan.request.context['domain'])
        return utils.render_with_links(self.collection, Whitelist.apply(roles))

    @pecan.expose('json')
    def get(self, role_id):
        keystone = Clients.keystone()
        role = keystone.roles.get(role_id)
        utils.check_permissions(role)
        return utils.render(self.resource, Whitelist.apply(role))


# vi: ts=4 et:

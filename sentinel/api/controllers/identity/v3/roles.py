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

from sentinel import utils
from sentinel.api.controllers.base import BaseController


class IdentityV3RolesController(BaseController):
    """Controller for the roles collection"""

    collection = u'roles'
    resource = u'role'

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    def get_all(self):
        roles = self.identity.roles.list(
            domain_id=pecan.request.context['domain'])
        return self.format_collection(roles)

    @pecan.expose('json')
    def get(self, role_id):
        role = self.identity.roles.get(role_id)
        utils.check_permissions(role)
        return self.format_resource(role)


# vi: ts=4 et:

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

import pecan
import pecan.decorators

from sentinel.api.controllers.base import BaseController
from sentinel.scope import Scope


class NetworkV2FloatingipsController(BaseController):

    service = u'network'
    resource = u'floatingip'
    collection = u'floatingips'

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    def get_all(self):
        floatingips = Scope.filter(self.network.list_floatingips())
        return self.format_collection(floatingips, links=False)

# vi: ts=4 et:


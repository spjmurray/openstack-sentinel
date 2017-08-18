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

"""Root controller for /identity"""

from sentinel.api.controllers.identity.v3 import root as v3

class IdentityController(object):
    def __init__(self):
        self.v3 = v3.IdentityV3Controller()

class Service(object):
    service_name = u'keystone'
    service_type = u'identity'
    service_endpoint = u'/identity/v3'

    @staticmethod
    def controller():
        return IdentityController()

# vi: ts=4 et:

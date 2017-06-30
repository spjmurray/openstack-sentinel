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

"""Root controller for /compute"""

import pecan

from sentinel.api.controllers.compute.v2 import root as v2

class ComputeController(object):
    @pecan.expose()
    def _lookup(self, version, *remainder):
        if version == 'v2':
            # Expect a project ID as part of the URL
            if not len(remainder):
                pecan.abort(400)
            pecan.request.context['project_id'] = remainder[0]
            return v2.ComputeV2Controller(), remainder[1:]
        pecan.abort(404)

# vi: ts=4 et:

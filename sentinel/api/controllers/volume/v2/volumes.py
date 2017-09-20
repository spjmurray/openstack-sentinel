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

from sentinel import utils
from sentinel.api.controllers import base
from sentinel.scope import Scope


class VolumeV2VolumesController(base.BaseController):

    service = u'volume'
    collection = u'volumes'
    resource = u'volume'

    def __init__(self):
        self._custom_actions = {
            'detail': ['GET'],
        }

    def _scoped_volumes(self):
        # If the client requested all projects return those within the
        # domain scope, otherwise scope to the specifc project.  This is undocumented!
        projects = Scope.projects() if utils.all_projects() else [pecan.request.token.project_id]

        # Load up detailed volume data as it contains project ID
        # NOTE: all_tenants is required, but not documented!!
        volumes = self.volume.volumes.list(search_opts={'all_tenants': 'True'})

        # Filter out volumes not in scope, stupid inconsistencies yet again
        volumes = [x for x in volumes if getattr(x, 'os-vol-tenant-attr:tenant_id') in projects]

        return utils.paginate(volumes, pecan.request.GET.get('marker'),
                              pecan.request.GET.get('limit'))

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    def get_all(self):
        volumes = self._scoped_volumes()
        volumes = [{'id': x.id, 'name': x.name} for x in volumes]
        return self.format_resource(volumes)

    @pecan.expose('json')
    def detail(self):
        volumes = self._scoped_volumes()
        return self.format_collection(volumes)

# vi: ts=4 et:


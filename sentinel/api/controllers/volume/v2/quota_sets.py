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

import copy
import pecan
import pecan.decorators

from sentinel.api.controllers import base
from sentinel.decorators import supported_queries, mutate_arguments


BAD_KEYS = ['id', 'tenant_id']

class VolumeV2QuotaSetsController(base.BaseController):

    service = u'volume'
    resource = u'quota_set'

    def __init__(self):
        self._custom_actions = {
            'defaults': ['GET'],
        }

    @pecan.expose('json')
    @supported_queries('usage')
    @mutate_arguments('identity.projects')
    def get(self, project):
        quota = self.volume.quotas.get(project.id, **pecan.request.GET)
        return self.format_resource(quota)

    @pecan.expose('json')
    @mutate_arguments('identity.projects')
    def put(self, project):
        updates = copy.copy(pecan.request.json['quota_set'])
        updates = {x: updates[x] for x in updates if x not in BAD_KEYS}
        quota = self.volume.quotas.update(project.id, **updates)
        return self.format_resource(quota)

    @pecan.expose('json')
    @mutate_arguments('identity.projects')
    def delete(self, project):
        self.volume.quotas.delete(project.id)
        pecan.response.status = 204

    @pecan.expose('json')
    @mutate_arguments('identity.projects')
    def defaults(self, project):
        quota = self.volume.quotas.defaults(project.id)
        return self.format_resource(quota)

# vi: ts=4 et:

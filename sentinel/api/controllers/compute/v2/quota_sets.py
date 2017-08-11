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

"""Root controller for /compute/v2/os-quota-sets"""

import pecan

from sentinel.api.controllers.base import BaseController
from sentinel.decorators import supported_queries, mutate_arguments


class ComputeV2QuotaSetsController(BaseController):
    """Controller for quota set resources"""

    service = u'compute'
    resource = u'quota_set'

    def __init__(self):
        self._custom_actions = {
            'defaults': ['GET'],
            'detail': ['GET'],
        }

    @pecan.expose('json')
    @supported_queries()
    @mutate_arguments('identity.projects')
    def get(self, project):
        quota = self.compute.quotas.get(project.id)
        return self.format_resource(quota)

    @pecan.expose('json')
    @supported_queries()
    @mutate_arguments('identity.projects')
    def put(self, project):
        quota = self.compute.quotas.update(project.id, **pecan.request.json.get('quota_set'))
        return self.format_resource(quota)

    @pecan.expose('json')
    @supported_queries()
    @mutate_arguments('identity.projects')
    def delete(self, project):
        self.compute.quotas.delete(project.id)
        pecan.response.status = 202

    @pecan.expose('json')
    @supported_queries()
    @mutate_arguments('identity.projects')
    def defaults(self, project):
        quota = self.compute.quotas.defaults(project.id)
        return self.format_resource(quota)

    @pecan.expose('json')
    @supported_queries()
    @mutate_arguments('identity.projects')
    def detail(self, project):
        quota = self.compute.quotas.get(project.id, detail=True)
        return self.format_resource(quota)

# vi: ts=4 et:

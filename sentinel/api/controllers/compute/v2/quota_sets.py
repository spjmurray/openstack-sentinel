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

import sentinel.utils as utils
from sentinel.api.controllers.base import BaseController


class ComputeV2QuotaSetsController(BaseController):
    """Controller for quota set resources"""

    resource = u'quota_set'

    def __init__(self):
        self._custom_actions = {
            'defaults': ['GET'],
            'detail': ['GET'],
        }

    @pecan.expose('json')
    def get(self, project_id):
        project = self.identity.projects.get(project_id)
        utils.check_permissions(project)
        quota = self.compute.quotas.get(project_id)
        return self.format_resource(quota)

    @pecan.expose('json')
    def put(self, project_id):
        project = self.identity.projects.get(project_id)
        utils.check_permissions(project)
        quota = self.compute.quotas.update(project_id, **pecan.request.json.get('quota_set'))
        return self.format_resource(quota)

    @pecan.expose('json')
    def delete(self, project_id):
        project = self.identity.projects.get(project_id)
        utils.check_permissions(project)
        self.compute.quotas.delete(project_id)
        pecan.response.status = 202

    @pecan.expose('json')
    def defaults(self, project_id):
        project = self.identity.projects.get(project_id)
        utils.check_permissions(project)
        quota = self.compute.quotas.defaults(project_id)
        return self.format_resource(quota)

    @pecan.expose('json')
    def detail(self, project_id):
        project = self.identity.projects.get(project_id)
        utils.check_permissions(project)
        quota = self.compute.quotas.get(project.id, detail=True)
        return self.format_resource(quota)

# vi: ts=4 et:

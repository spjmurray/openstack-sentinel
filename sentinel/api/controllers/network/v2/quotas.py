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

from sentinel.api.controllers import base
from sentinel.decorators import supported_queries, mutate_arguments
from sentinel.scope import Scope


class NetworkV2QuotasController(base.BaseController):

    resource = u'quota'
    collection = u'quotas'

    def __init__(self):
        self._custom_actions = {
            'default': ['GET'],
        }

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    @supported_queries()
    def get_all(self):
        quotas = Scope.filter(self.network.list_quotas())
        return self.format_collection(quotas, links=False)

    @pecan.expose('json')
    @mutate_arguments('identity.projects')
    def get(self, project):
        quota = self.network.show_quota(project.id)
        return self.format_resource(quota)

    @pecan.expose('json')
    @mutate_arguments('identity.projects')
    def put(self, project):
        quota = self.network.update_quota(project.id, body=pecan.request.json)
        return self.format_resource(quota)

    @pecan.expose('json')
    @mutate_arguments('identity.projects')
    def delete(self, project):
        self.network.delete_quota(project.id)
        pecan.response.status = 204

    @pecan.expose('json')
    @mutate_arguments('identity.projects')
    def default(self, project):
        quota = self.network.show_quota_default(project.id)
        return self.format_resource(quota)

# vi: ts=4 et:

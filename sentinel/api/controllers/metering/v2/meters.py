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

# pylint: disable=invalid-name

import wsme.types
import wsmeext.pecan

from sentinel.api.controllers import base
from sentinel.scope import Scope


class Query(wsme.types.DynamicBase):
    field = wsme.types.text
    op = wsme.types.text
    value = wsme.types.text
    type = wsme.types.text


class Sample(wsme.types.DynamicBase):
    source = wsme.types.text
    counter_name = wsme.types.text
    counter_unit = wsme.types.text
    counter_volume = float
    user_id = wsme.types.text
    project_id = wsme.types.text
    resource_id = wsme.types.text
    timestamp = wsme.types.text
    recorded_at = wsme.types.text
    resource_metadata = {wsme.types.text: wsme.types.text}
    message_id = wsme.types.text


class MeteringV2MetersController(base.BaseController):

    @wsmeext.pecan.wsexpose([Sample], str, [Query], int)
    def get(self, meter, q=None, limit=None):
        queries = [vars(query) for query in q] if q else None
        samples = self.metering.samples.list(meter, queries, limit)
        samples = Scope.filter(samples)
        return [Sample(**sample.to_dict()) for sample in samples]

# vi: ts=4 et:

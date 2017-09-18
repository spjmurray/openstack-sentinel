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

from sentinel.api.controllers.volume.v2 import quota_sets
from sentinel.api.controllers.volume.v2 import volumes


class VolumeV2Controller(object):
    def __init__(self):
        self.volumes = volumes.VolumeV2VolumesController()


pecan.route(VolumeV2Controller, 'os-quota-sets', quota_sets.VolumeV2QuotaSetsController())

# vi: ts=4 et:

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

import setuptools

setuptools.setup(
    name = 'sentinel',
    version = '0.0.1',
    packages = setuptools.find_packages(),
    entry_points = {
        'oslo.config.opts': [
            'sentinel = sentinel.conf.opts:list_opts',
        ],
        'sentinel.services': [
            'identity = sentinel.api.controllers.identity.root:Service',
            'compute = sentinel.api.controllers.compute.root:Service',
            'network = sentinel.api.controllers.network.root:Service',
            'volume = sentinel.api.controllers.volume.root:Service',
            'metering = sentinel.api.controllers.metering.root:Service',
        ],
    }
)

# vi: ts=4 et:

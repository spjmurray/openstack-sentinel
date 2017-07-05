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

"""Whitelist fields from OpenStack resources"""

import inspect
import pecan

class Whitelist(object):
    
    @staticmethod
    def apply(resources):
        # Get the calling module name, this will determine the whitelist key
        # to extract from the configuration
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        name = module.__name__

        # Load the whitelist
        whitelist = pecan.request.context['conf'].get('whitelist', name)

        def whitelister(resource):
            resource = resource.to_dict()
            return { k: resource[k] for k in resource if k in whitelist }

        # Handle collections
        if isinstance(resources, list):
            return map(whitelister, resources)

        # Or single resources
        return whitelister(resources)

# vi: ts=4 et:

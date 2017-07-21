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

import pecan

class Whitelist(object):

    @staticmethod
    def apply(resources, name):
        whitelist = pecan.request.context['conf'].get('whitelist', name).split(',')

        # Just pass everything through
        def null_whitelister(resource):
            if not isinstance(resource, dict):
                resource = resource.to_dict()
            return resource

        # Selectively return only whitelisted key/value pairs
        def whitelister(resource):
            if not isinstance(resource, dict):
                resource = resource.to_dict()
            return {k: resource[k] for k in resource if k in whitelist}

        # Select the processing engine
        if '*' in whitelist:
            proc = null_whitelister
        else:
            proc = whitelister

        # Handle collections
        if isinstance(resources, list):
            return [proc(x) for x in resources]

        # Or single resources
        return proc(resources)

# vi: ts=4 et:

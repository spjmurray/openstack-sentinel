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
import pecan.rest

from sentinel.clients import Clients
from sentinel.whitelist import Whitelist


class BaseController(pecan.rest.RestController):
    """Common REST controller library functions"""

    resource = None
    collection = None

    def _get_client(self, name):
        """Get a cached client or lazily create a new one"""
        client = pecan.request.context.get(name)
        if not client:
            client = getattr(Clients, name)()
            pecan.request.context[name] = client
        return client

    @property
    def identity(self):
        """Get an identity client"""
        return self._get_client('identity')

    @property
    def compute(self):
        """Get a compute client"""
        return self._get_client('compute')

    @property
    def network(self):
        """Get a network client"""
        return self._get_client('network')

    def format_resource(self, data, resource=None):
        """Format a resource"""
        if not resource:
            resource = self.resource
        payload = {
            resource: Whitelist.apply(data, resource),
        }
        return payload

    def format_collection(self, data, resource=None, collection=None, links=True):
        """Format a colelction of resources"""
        if not resource:
            resource = self.resource
        if not collection:
            collection = self.collection
        payload = {
            collection: Whitelist.apply(data, resource),
        }
        if links:
            payload[u'links'] = {
                u'next': None,
                u'previous': None,
                u'self': pecan.request.path_url,
            }
        return payload

# vi: ts=4 et:

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

def check_permissions(*resources):
    """Check we have access to this resource or raise an error"""
    for resource in resources:
        if resource.domain_id != pecan.request.context['domain']:
            pecan.abort(403, 'unauthorized access a resource outside of your domain')

def render(entity, data):
    """Render a response for an entity type"""
    payload = {
        entity: data,
    }
    return payload

def render_with_links(entity, data):
    """Render a response for an entity type with links"""
    payload = {
        u'links': {
            u'next': None,
            u'previous': None,
            u'self': pecan.request.path_url,
        },
        entity: data,
    }
    return payload

# vi: ts=4 et:

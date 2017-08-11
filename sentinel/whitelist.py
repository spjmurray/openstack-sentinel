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

from oslo_config import cfg, types
import pecan

OPTS = [
    cfg.ListOpt('identity_user',
                item_type=types.String(),
                default=['description', 'domain_id', 'email', 'enabled', 'id', 'name'],
                help='List of fields to return for user resources from the identity service'),
    cfg.ListOpt('identity_role',
                item_type=types.String(),
                default=['id', 'name'],
                help='List of fields to return for role resources from the identity service'),
    cfg.ListOpt('identity_group',
                item_type=types.String(),
                default=['description', 'domain_id', 'id', 'name'],
                help='List of fields to return for group resources from the identity service'),
    cfg.ListOpt('identity_project',
                item_type=types.String(),
                default=['description', 'domain_id', 'enabled', 'id', 'is_domain', 'name',
                         'parents', 'parent_id', 'subtree'],
                help='List of fields to return for project resources from the identity service'),
    cfg.ListOpt('compute_quota_set',
                item_type=types.String(),
                default=['*'],
                help='List of fields to return for quota_sets from the compute service'),
    cfg.ListOpt('compute_server',
                item_type=types.String(),
                default=['created', 'flavor', 'id', 'name', 'status', 'tenant_id', 'user_id'],
                help='List of fields to return for server resources from the compute service'),
    cfg.ListOpt('volume_quota_set',
                item_type=types.String(),
                default=['*'],
                help='List of fields to return for quota_sets from the volume service'),
    cfg.ListOpt('network_quota',
                item_type=types.String(),
                default=['*'],
                help='List of fields to return for quotas from the networking service'),
]

OPTS_GROUP = cfg.OptGroup('whitelist',
                          title='Resource Whitelist',
                          help='Controls which resource fields are returned to the IdP')


class Whitelist(object):

    @staticmethod
    def apply(resources, service, resource):
        whitelist = getattr(pecan.request.conf.whitelist, service + '_' + resource)

        # Just pass everything through
        def null_whitelister(resource):
            return resource.to_dict()

        # Selectively return only whitelisted key/value pairs
        def whitelister(resource):
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

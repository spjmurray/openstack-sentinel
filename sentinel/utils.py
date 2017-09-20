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

import oslo_utils.strutils
import pecan

from sentinel.clients import Resource


def check_permissions(*resources):
    """Check we have access to this resource or raise an error"""
    for resource in resources:
        if resource.domain_id != pecan.request.domain_id:
            pecan.abort(403, 'unauthorized access a resource outside of your domain')


def all_projects():
    """Do we want all projects in our domain"""

    # A basic copy of nova API
    flag = pecan.request.GET.get('all_tenants')
    if flag:
        return oslo_utils.strutils.bool_from_string(flag, True)

    # An empty string is considered consent
    return 'all_tenants' in pecan.request.GET


def unglancify(resources):
    """Make glance resources and collection not special snowflakes"""

    # Glance responses are warlock objects which are dict subclasses but implement
    # the pretty __getattr__() method (e.g. don't have the to_dict() method like
    # every other client - neutron being the other exception, but that's handled
    # by the client class decorator). We wrap as a Resources.
    return [Resource(x) for x in resources]


# vi: ts=4 et:

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

"""Handlers for domain scoping"""

import pecan

from sentinel.clients import Clients


class Scope(object):
    @staticmethod
    def projects():
        """Return a list of projects within our domain scope.  This is
           used to determine whether we can create tokens scoped to a
           specific project, which resources in a collection to list and
           whether an action can be performed on a resource"""

        # Domain is mapped from the certificate DN
        domain = pecan.request.domain_id
        identity = Clients.identity()

        # Get a domain filtered list of projects and return the IDs
        # Todo: needs extending to support nested domains
        projects = identity.projects.list(domain=domain)
        return [x.id for x in projects]

    @classmethod
    def filter(cls, resources, projects=None, key=None):
        """Filter collections based on project ID"""

        # Nothing to do
        if not resources:
            return []

        # Gather projects if not explicitly stated
        if not projects:
            projects = cls.projects()

        # Hack around the fact that OpenStack is a totally inconsistent mess
        if not key:
            key = 'project_id'
            if not hasattr(resources[0], key):
                key = 'tenant_id'

        return [x for x in resources if getattr(x, key) in projects]

# vi: ts=4 et:

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

import functools

import pecan

from sentinel import utils


def supported_queries(*supported):
    '''
    Checks for whitelisted query parameters
    '''
    def decorate(func):
        @functools.wraps(func)
        def call(*args):
            unsupported = frozenset(pecan.request.GET.keys()) - frozenset(supported)
            if unsupported:
                pecan.abort(400, 'Unsupported query parameters %s' % ','.join(unsupported))
            return func(*args)
        return call
    return decorate

def mutate_arguments(*types):
    '''
    Converts resource IDs into concrete types and performs permissions checks
    '''
    def decorate(func):
        @functools.wraps(func)
        def call(self, *args):
            if len(types) != len(args):
                pecan.abort(500, 'Argument list lengths differ')
            def resolve_getter(path):
                '''Takes a path e.g. 'identity.users' and return the object from the class'''
                path = path.split('.')
                obj = self
                while path:
                    obj = getattr(obj, path.pop(0))
                return obj
            # Map from object IDs to resource objects
            resources = [resolve_getter(x[0]).get(x[1]) for x in zip(types, args)]
            # Check we have permission to access the resource
            utils.check_permissions(*resources)
            return func(self, *resources)
        return call
    return decorate

# vi: ts=4 et:

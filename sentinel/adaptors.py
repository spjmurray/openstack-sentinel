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

import copy

class Resource(object):
    """Base reource type conforming to the keystone/nova API"""

    def __init__(self, info):
        self._info = info
        for i in info:
            setattr(self, i, info[i])

    def to_dict(self):
        return copy.deepcopy(self._info)


def rawclientadaptor(cls):
    """Wraps clients returning raw data so they return resources"""

    class Wrapper(object):
        def __init__(self, *args, **kwargs):
            self.wrapped = cls(*args, **kwargs)

        def __getattr__(self, name):
            # Look for functions being accessed
            attr = getattr(self.wrapped, name)
            if not callable(attr):
                return attr

            # And wrap them up so we can post process the results
            def call(*args, **kwargs):
                """
                Decorator which looks for raw OpenStack responses e.g. '{"routers":[...]}'
                And returns a single or list of Resource types for single resources and
                collections respectively
                """
                ret = attr(*args, **kwargs)
                if isinstance(ret, dict):
                    res = ret[ret.keys()[0]]
                    if isinstance(res, list):
                        return [Resource(x) for x in res]
                    return Resource(res)
                return ret

            return call

    return Wrapper

# vi: ts=4 et:

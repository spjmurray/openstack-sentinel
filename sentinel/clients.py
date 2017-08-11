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

"""
Simple wrappers around OpenStack client libraries
"""

import copy
from ceilometerclient.v2 import client as metering_client
from cinderclient.v2 import client as volume_client
from keystoneauth1 import session
from keystoneauth1.identity import v3
from keystoneclient.v3 import client as identity_client
from neutronclient.v2_0 import client as network_client
from novaclient import client as compute_client
from oslo_config import cfg
import pecan


OPTS = [
    cfg.URIOpt('auth_url',
               schemes=['https'],
               required=True,
               help='URL of the SP identity service'),
    cfg.StrOpt('username',
               required=True,
               help='Username of an admin account on the SP cloud'),
    cfg.StrOpt('password',
               required=True,
               secret=True,
               help='Password of an admin account on the SP cloud'),
    cfg.StrOpt('user_domain_name',
               default='default',
               help='Domain of an admin account user on the SP cloud'),
    cfg.StrOpt('project_name',
               required=True,
               help='Project of an admin user on the SP cloud'),
    cfg.StrOpt('project_domain_name',
               default='default',
               help='Domain of an admin project on the SP cloud'),
]

OPTS_GROUP = cfg.OptGroup('identity',
                          title='Service Provider Identity Credentials',
                          help='Admin access to the SP cloud')


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


@rawclientadaptor
class NeutronClient(network_client.Client):
    """Wrapped neutron client which returns Resources not raw data"""
    pass


class Clients(object):
    """Obtain various OpenStack clients"""

    @staticmethod
    def _session():
        """Creates an OpenStack session from configuration data"""
        conf = pecan.request.conf
        auth = v3.Password(auth_url=conf.identity.auth_url,
                           username=conf.identity.username,
                           password=conf.identity.password,
                           user_domain_name=conf.identity.user_domain_name,
                           project_name=conf.identity.project_name,
                           project_domain_name=conf.identity.project_domain_name)
        return session.Session(auth=auth)

    @classmethod
    def identity(cls):
        """Creates a Keystone client"""
        return identity_client.Client(session=cls._session())

    @classmethod
    def compute(cls):
        """Creates a Nova client"""
        return compute_client.Client(2, session=cls._session())

    @classmethod
    def network(cls):
        """Creates a Neutron client"""
        return NeutronClient(session=cls._session())

    @classmethod
    def volume(cls):
        """Creates a Clinder client"""
        return volume_client.Client(session=cls._session())

    @classmethod
    def metering(cls):
        """Creates a Ceilometer client"""
        return metering_client.Client(session=cls._session())

# vi: ts=4 et:

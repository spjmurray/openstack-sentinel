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

from ceilometerclient.v2 import client as metering_client
from cinderclient.v2 import client as volume_client
from glanceclient.v2 import client as image_client
from keystoneauth1 import session
from keystoneauth1.identity import v3
from keystoneclient.v3 import client as identity_client
from neutronclient.v2_0 import client as network_client
from novaclient import client as compute_client
from oslo_config import cfg
import pecan

from sentinel import adaptors


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


@adaptors.rawclientadaptor
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

    @classmethod
    def image(cls):
        """Creates a Glance client"""
        return image_client.Client(session=cls._session())

# vi: ts=4 et:

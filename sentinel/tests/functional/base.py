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

import ConfigParser
from cinderclient.v2 import client as volume_client
from keystoneauth1 import session
from keystoneauth1.identity import v3
from keystoneclient.v3 import client as identity_client
from neutronclient.v2_0 import client as network_client
from novaclient import client as compute_client
import testtools

class BaseClient(object):
    """Base client which creates and caches clients"""

    def __init__(self, conf):
        self.conf = conf
        self._identity = None
        self._compute = None
        self._network = None
        self._volume = None

    @property
    def identity(self):
        if not self._identity:
            self._identity = identity_client.Client(session=self._session())
        return self._identity

    @property
    def compute(self):
        if not self._compute:
            self._compute = compute_client.Client(2, session=self._session())
        return self._compute

    @property
    def network(self):
        if not self._network:
            self._network = network_client.Client(session=self._session())
        return self._network

    @property
    def volume(self):
        if not self._volume:
            self._volume = volume_client.Client(session=self._session())
        return self._volume

    def _session(self):
        pass

class SentinelClient(BaseClient):
    """Sentinel client which creates sessions for sentinel"""

    def __init__(self, conf):
        super(SentinelClient, self).__init__(conf)

    def _session(self):
        auth = v3.Password(auth_url=self.conf.get('sentinel_auth', 'auth_uri'))
        return session.Session(auth=auth,
                               verify=self.conf.get('sentinel_auth', 'tls_ca'),
                               cert=(self.conf.get('sentinel_auth', 'tls_cert'),
                                     self.conf.get('sentinel_auth', 'tls_key')))


class OpenStackClient(BaseClient):
    """OpenStack client that creates sessions for native clouds"""

    def __init__(self, conf):
        super(OpenStackClient, self).__init__(conf)

    def _session(self):
        required = ['auth_url', 'username', 'password', 'user_domain_name',
                    'project_name', 'project_domain_name']
        params = {x: self.conf.get('keystone_authtoken', x) for x in required}
        auth = v3.Password(**params)
        return session.Session(auth=auth)


class BaseTestCase(testtools.TestCase):

    def setUp(self):
        super(BaseTestCase, self).setUp()

        # Load up the configuration
        conf = ConfigParser.ConfigParser()
        conf.read('/etc/sentinel/sentinel-test.conf')

        # Register client managers
        self.sentinel = SentinelClient(conf)
        self.openstack = OpenStackClient(conf)


# vi: ts=4 et:

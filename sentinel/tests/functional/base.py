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

import testtools

from ceilometerclient.v2 import client as metering_client
from cinderclient.v2 import client as volume_client
from glanceclient.v2 import client as image_client
from keystoneauth1 import session
from keystoneauth1.identity import v3
from keystoneclient.v3 import client as identity_client
from neutronclient.v2_0 import client as network_client
from novaclient import client as compute_client
from oslo_config import cfg
from sentinel.conf import opts
from sentinel import adaptors

OPTS = [
    cfg.URIOpt('auth_url',
               help='URL of the sentinel identity service'),
    cfg.StrOpt('tls_ca',
               help='CA certificate of sentinel server'),
    cfg.StrOpt('tls_cert',
               help='Certificate for the sentinel client'),
    cfg.StrOpt('tls_key',
               help='Private key for the sentinel client'),
]

OPTS_GROUP = cfg.OptGroup('functional_test',
                          title='Sentinel Authentication',
                          help='Access credentials for a sentinel instance used in testing')


@adaptors.rawclientadaptor
class NeutronClient(network_client.Client):
    """Wrapped neutron client which returns Resources not raw data"""
    pass


class BaseClient(object):
    """Base client which creates and caches clients"""

    def __init__(self):

        # Load up the configuration
        self.conf = opts.configure()

        self._identity = None
        self._compute = None
        self._network = None
        self._volume = None
        self._metering = None
        self._image = None

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
            self._network = NeutronClient(session=self._session())
        return self._network

    @property
    def volume(self):
        if not self._volume:
            self._volume = volume_client.Client(session=self._session())
        return self._volume

    @property
    def metering(self):
        if not self._metering:
            self._metering = metering_client.Client(session=self._session())
        return self._metering

    @property
    def image(self):
        if not self._image:
            self._image = image_client.Client(session=self._session())
        return self._image

    def _session(self):
        pass

class SentinelClient(BaseClient):
    """Sentinel client which creates sessions for sentinel"""

    def __init__(self):
        super(SentinelClient, self).__init__()

    def _session(self):
        auth = v3.Password(auth_url=self.conf.functional_test.auth_url)
        return session.Session(auth=auth,
                               verify=self.conf.functional_test.tls_ca,
                               cert=(self.conf.functional_test.tls_cert,
                                     self.conf.functional_test.tls_key))


class OpenStackClient(BaseClient):
    """OpenStack client that creates sessions for native clouds"""

    def __init__(self):
        super(OpenStackClient, self).__init__()

    def _session(self):
        auth = v3.Password(auth_url=self.conf.identity.auth_url,
                           username=self.conf.identity.username,
                           password=self.conf.identity.password,
                           user_domain_name=self.conf.identity.user_domain_name,
                           project_name=self.conf.identity.project_name,
                           project_domain_name=self.conf.identity.project_domain_name)
        return session.Session(auth=auth)


class FederatedUserClient(BaseClient):
    """Client based on OpenStack client objects"""

    def __init__(self, user, project):
        super(FederatedUserClient, self).__init__()
        self.user = user
        self.project = project

    def _session(self):
        auth = v3.Password(auth_url=self.conf.identity.auth_url,
                           user_id=self.user.id,
                           password='password',
                           project_id=self.project.id)
        return session.Session(auth=auth)


class BaseTestCase(testtools.TestCase):

    def setUp(self):
        super(BaseTestCase, self).setUp()

        # Register client managers
        self.sentinel = SentinelClient()
        self.openstack = OpenStackClient()


# vi: ts=4 et:

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
from keystoneauth1 import session
from keystoneauth1.identity import v3
from keystoneclient.v3 import client
import testtools

class KeystoneBaseTestCase(testtools.TestCase):
    def setUp(self):
        super(KeystoneBaseTestCase, self).setUp()

        # Load up the configuration
        conf = ConfigParser.ConfigParser()
        conf.read('/etc/sentinel/sentinel-test.conf')

        # Create a keystone client pointing at the actual SP instance
        auth = v3.Password(auth_url=conf.get('keystone_authtoken', 'auth_uri'),
                           username=conf.get('keystone_authtoken', 'username'),
                           password=conf.get('keystone_authtoken', 'password'),
                           user_domain_name=conf.get('keystone_authtoken', 'user_domain_name'),
                           project_name=conf.get('keystone_authtoken', 'project_name'),
                           project_domain_name=conf.get('keystone_authtoken', 'project_domain_name'))
        sess = session.Session(auth=auth)
        self.keystone = client.Client(session=sess)

        # Create a keystone client pointing at sentinel
        auth = v3.Password(auth_url=conf.get('sentinel_auth', 'auth_uri'))
        sess = session.Session(auth=auth,
                               verify=conf.get('sentinel_auth', 'tls_ca'),
                               cert=(conf.get('sentinel_auth', 'tls_cert'),
                                     conf.get('sentinel_auth', 'tls_key')))
        self.sentinel = client.Client(session=sess)

# vi: ts=4 et:

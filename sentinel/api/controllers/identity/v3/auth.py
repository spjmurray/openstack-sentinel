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

from datetime import datetime, timedelta
import logging
import pecan

from sentinel.scope import Scope
from sentinel.token import Token

LOG = logging.getLogger(__name__)


class IdentityV3AuthController(object):

    @pecan.expose('json')
    def tokens(self):
        # X.509 handles authentication and identification, however we need to
        # remember the project scope somehow.  As we are stateless we cannot
        # cache this in a database, so we encode this in the token.
        try:
            project = pecan.request.json['auth']['scope']['project']['id']
            token = Token(project_id=project)
            LOG.info('Scoped authentication request by %s for %s',
                     pecan.request.context['user'], project)
        except KeyError:
            token = Token()
            LOG.info('Domain scoped authentication request by %s',
                     pecan.request.context['user'])

        # Reject scoping to a project not in our domain
        if token.project_id and token.project_id not in Scope.projects():
            pecan.abort(404, 'project not in found in this domain')

        # Generate the response.  The official client library checks the time stamps
        # so these are required, Fog requires that the user has a project which it
        # caches away for various purposes.  The other important bit is the service
        # catalog pointing back to ourselves.
        issued = datetime.now()
        expires = issued + timedelta(0, 0, 0, 0, 0, 1, 0)
        identity_base = '{}/identity/v3'.format(pecan.request.host_url)
        compute_base = '{}/compute/v2'.format(pecan.request.host_url)
        networking_base = '{}/network'.format(pecan.request.host_url)
        volume_base = '{}/volume/v2'.format(pecan.request.host_url)

        payload = {
            'token': {
                'issued_at': issued.isoformat(),
                'expires_at': expires.isoformat(),
                'user': {
                    'project': 'required-by-fog',
                },
                'catalog': [
                    {
                        'name': 'keystone',
                        'type': 'identity',
                        'endpoints': [
                            {
                                'interface': 'public',
                                'url': identity_base,
                            },
                            {
                                'interface': 'admin',
                                'url': identity_base,
                            }
                        ]
                    },
                    {
                        'name': 'nova',
                        'type': 'compute',
                        'endpoints': [
                            {
                                'interface': 'public',
                                'url': compute_base,
                            }
                        ]
                    },
                    {
                        'name': 'neutron',
                        'type': 'network',
                        'endpoints': [
                            {
                                'interface': 'public',
                                'url': networking_base,
                            }
                        ]
                    },
                    {
                        'name': 'cinderv2',
                        'type': 'volumev2',
                        'endpoints': [
                            {
                                'interface': 'public',
                                'url': volume_base,
                            },
                        ]
                    },
                ]
            }
        }

        pecan.response.status = 201
        pecan.response.headers['X-Subject-Token'] = token.marshal()
        return payload

# vi: ts=4 et:

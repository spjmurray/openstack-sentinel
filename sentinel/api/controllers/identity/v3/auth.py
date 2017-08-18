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
from stevedore import extension

from sentinel.scope import Scope
from sentinel.token import Token

LOG = logging.getLogger(__name__)

ENDPOINT_INTERFACES = [u'public', u'internal', u'admin']


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
                     pecan.request.user, project)
        except KeyError:
            token = Token()
            LOG.info('Domain scoped authentication request by %s',
                     pecan.request.user)

        # Reject scoping to a project not in our domain
        if token.project_id and token.project_id not in Scope.projects():
            pecan.abort(404, 'project not in found in this domain')

        # Generate the response.  The official client library checks the time stamps
        # so these are required, Fog requires that the user has a project which it
        # caches away for various purposes.  The other important bit is the service
        # catalog pointing back to ourselves.
        issued = datetime.now()
        expires = issued + timedelta(0, 0, 0, 0, 0, 1, 0)

        # Use stevedor to find all extensions and dynamically build the catalog
        # from static data contained in each service object
        manager = extension.ExtensionManager(
            namespace='sentinel.services',
            invoke_on_load=True)

        def get_catalog(ext):
            endpoints = []
            for interface in ENDPOINT_INTERFACES:
                endpoints.append({
                    u'interface': interface,
                    u'url': pecan.request.host_url + ext.obj.service_endpoint})
            payload = {
                u'name': ext.obj.service_name,
                u'type': ext.obj.service_type,
                u'endpoints': endpoints,
            }
            return payload

        payload = {
            u'token': {
                u'issued_at': issued.isoformat(),
                u'expires_at': expires.isoformat(),
                u'user': {
                    u'project': 'required-by-fog',
                },
                u'catalog': manager.map(get_catalog),
            }
        }

        pecan.response.status = 201
        pecan.response.headers['X-Subject-Token'] = token.marshal()
        return payload

# vi: ts=4 et:

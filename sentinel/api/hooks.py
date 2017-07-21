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

"""Middleware hooks"""

import json
import logging
import time
import traceback

import keystoneauth1.exceptions
import neutronclient.common.exceptions
import pecan
import pecan.hooks
import webob

from sentinel.token import Token

LOG = logging.getLogger(__name__)

class ConfigHook(pecan.hooks.PecanHook):
    """Attaches a configuration object to requests"""

    def __init__(self, conf):
        super(ConfigHook, self).__init__()
        self.conf = conf

    def on_route(self, state):
        state.request.context['conf'] = self.conf

class DomainHook(pecan.hooks.PecanHook):
    """Translates X.509 DN into a domain ID and attaches to requests"""

    def on_route(self, state):
        # Load mapping each time so we don't have to restart apache
        with open('/etc/sentinel/domain_map.json') as f:
            mapping = json.load(f)
        # Extract the username from the certificate DN and attach to the request
        user = state.request.environ['SSL_CLIENT_S_DN'].split('=')[1]
        state.request.context['user'] = user
        # Try find a valid mapping from user to domain ID
        try:
            state.request.context['domain'] = mapping[user]
        except KeyError:
            pecan.abort(401)

class TokenHook(pecan.hooks.PecanHook):
    """Unmarshal a token and attach to requests"""

    def on_route(self, state):
        try:
            token = pecan.request.environ['X-Subject-Token']
            state.request.context['token'] = Token.unmarshal(token)
        except KeyError:
            # This will legitimately fault on token requests
            state.request.context['token'] = None

class LoggerHook(pecan.hooks.PecanHook):
    """Print out requests in the log"""

    def on_route(self, state):
        state.request.context['start'] = time.time()

    def after(self, state):
        delta = time.time() - state.request.context['start']
        LOG.info('%s "%s %s" status: %d time: %0.3f',
                 state.request.client_addr,
                 state.request.method,
                 state.request.url,
                 state.response.status_code,
                 delta)

class ExceptionHook(pecan.hooks.PecanHook):
    """Catch exceptions"""

    def on_error(self, state, exc):
        LOG.warning('Exception %s: %s', exc.__class__.__name__, exc.message)
        LOG.warning('%s', traceback.format_exc(exc))

        # If it's a native webob exception then pecan has already done its own
        # thing and filled in the body for us.  We want to reset this so that
        # the exception's __call__ method generated a webob native body which
        # is cpm[atible with OpenStack clients
        if issubclass(exc.__class__, webob.Response):
            del exc.body
            return exc

        # Translate openstack client exceptions back into webob
        if issubclass(exc.__class__, keystoneauth1.exceptions.HttpError):
            return webob.Response(exc.message, status=exc.http_status)
        if issubclass(exc.__class__, neutronclient.common.exceptions.NeutronClientException):
            return webob.Response(exc.message, status=exc.status_code)

        LOG.error('Unhandled exception')

# vi: ts=4 et:

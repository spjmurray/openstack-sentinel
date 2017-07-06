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

import keystoneauth1.exceptions
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
        #LOG.info('{} {}'.format(state.request.method, state.request.path))

    def after(self, state):
        delta = time.time() - state.request.context['start']
        LOG.info('%s "%s %s" status: %d time: %0.3f',
                 state.request.client_addr,
                 state.request.method,
                 state.request.path,
                 state.response.status_code,
                 delta)

class ExceptionHook(pecan.hooks.PecanHook):
    """Catch exceptions"""

    def on_error(self, state, exc):
        if isinstance(exc, webob.exc.HTTPNotFound):
            return
        if issubclass(exc.__class__, keystoneauth1.exceptions.HttpError):
            LOG.error('caught exception %s', exc.message)
            return webob.Response(exc.message, status=exc.http_status)
        LOG.error('unhandled exception %s', exc.__class__.__name__)

# vi: ts=4 et:

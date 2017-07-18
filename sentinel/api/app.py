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

"""Main application entry"""

import ConfigParser
import logging

import pecan
from sentinel.api import hooks

LOG = logging.getLogger(__name__)


class LogFilter(logging.Filter):
    def filter(self, record):
        try:
            record.user = pecan.request.context.get('domain') or '-'
        except AttributeError:
            record.user = '-'
        return True


def get_app():
    """Load configuration, register middleware hooks and create the application"""

    conf = ConfigParser.ConfigParser()
    conf.read('/etc/sentinel/sentinel.conf')

    formater = logging.Formatter(
        fmt='%(asctime)s.%(msecs)03d %(process)d %(levelname)s %(name)s [%(user)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    handler = logging.FileHandler('/var/log/sentinel/sentinel.log')
    handler.setFormatter(formater)
    handler.addFilter(LogFilter())

    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)

    LOG.info('Sentinel starting ...')

    app_hooks = [
        hooks.ConfigHook(conf),
        hooks.LoggerHook(),
        hooks.DomainHook(),
        hooks.TokenHook(),
        hooks.ExceptionHook(),
    ]

    return pecan.make_app(
        'sentinel.api.controllers.root.RootController',
        hooks=app_hooks,
    )

# vi: ts=4 et:

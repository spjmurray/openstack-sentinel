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

import logging

from oslo_config import cfg
import pecan

OPTS = [
    cfg.StrOpt('log_level',
               default='INFO',
               choices=['INFO', 'WARN', 'WARNING', 'CRITICAL', 'ERROR', 'FATAL', 'DEBUG'],
               help='Level to emit logs at.  Maps directly to those in the logging package'),
]

OPTS_GROUP = None


class LogFilter(logging.Filter):
    def filter(self, record):
        record.user = getattr(pecan.request, 'domain_id', '-')
        return True


def init_logging(conf):
    formater = logging.Formatter(
        fmt='%(asctime)s.%(msecs)03d %(process)d %(levelname)s %(name)s [%(user)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    handler = logging.FileHandler('/var/log/sentinel/sentinel.log')
    handler.setFormatter(formater)
    handler.addFilter(LogFilter())

    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(getattr(logging, conf.log_level, 'INFO'))


# vi: ts=4 et:

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

import importlib

from oslo_config import cfg

MODULES = [
    'sentinel.clients',
    'sentinel.log',
    'sentinel.tests.functional.base',
    'sentinel.whitelist',
]

def list_opts():
    opts = []
    for module_name in MODULES:
        module = importlib.import_module(module_name)

        group = None
        if module.OPTS_GROUP:
            group = module.OPTS_GROUP.name

        opts.append((group, module.OPTS))
    return opts


def configure():
    conf = cfg.ConfigOpts()
    for module_name in MODULES:
        module = importlib.import_module(module_name)

        group = None
        if module.OPTS_GROUP:
            group = module.OPTS_GROUP.name
            conf.register_group(module.OPTS_GROUP)

        conf.register_opts(module.OPTS, group=group)

    conf([], project='sentinel')
    return conf


# vi: ts=4 et:

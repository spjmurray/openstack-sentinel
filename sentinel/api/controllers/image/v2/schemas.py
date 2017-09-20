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

import pecan
import pecan.decorators

from sentinel.api.controllers.base import BaseController


class ImageV2SchemasImageController(BaseController):

    @pecan.expose('json')
    def get(self):
        # Rather than return a schema resource (e.g. {"schema": {}}), glance
        # returns a raw blob of JSON, simply unmarshal from its container
        # bypassing all format_* methods and let pecan render
        return self.image.schemas.get('image').raw()


class ImageV2SchemasController(object):

    # Don't be tempted to make this a RestController and have a
    # get(self, target) handler, one of the targets happens to
    # be 'image' which the routing picks up as the image client!
    def __init__(self):
        self.image = ImageV2SchemasImageController()

# vi: ts=4 et:


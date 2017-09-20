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

from sentinel import utils
from sentinel.api.controllers.base import BaseController
from sentinel.scope import Scope


class ImageV2ImagesController(BaseController):

    service = u'image'
    collection = u'images'
    resource = u'image'

    def _scoped_images(self):
        projects = Scope.projects()
        images = utils.unglancify(self.image.images.list())

        # Filter out images not in scope, stupid inconsistencies yet again
        images = [x for x in images if x.owner in projects]

        return utils.paginate(images, pecan.request.GET.get('marker'),
                              pecan.request.GET.get('limit'))

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    def get_all(self):
        images = self._scoped_images()
        return self.format_collection(images)

# vi: ts=4 et:


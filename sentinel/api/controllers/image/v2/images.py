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

        # If the request features a marker reject all images upto and including
        # that ID
        marker = pecan.request.GET.get('marker')
        if marker:
            index = 0
            for image in images:
                if image.id == marker:
                    break
                index += 1
            if index == len(images):
                pecan.abort(400, 'Unable to locate marker')
            images = images[index+1:]

        # If the request features a limit return upto that many images
        limit = pecan.request.GET.get('limit')
        if limit:
            images = images[:int(limit)]

        return images

    @pecan.expose('json')
    @pecan.decorators.accept_noncanonical
    def get_all(self):
        images = self._scoped_images()
        return self.format_collection(images)

# vi: ts=4 et:


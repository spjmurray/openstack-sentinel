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

from sentinel.tests.functional import base, matchers
from sentinel.tests.functional import client_fixtures as fixtures


class ImageV2ImagesTestCase(base.BaseTestCase):

    def test_image_list(self):
        grant = self.useFixture(fixtures.UserProjectGrant(self.sentinel))
        federated = base.FederatedUserClient(grant.user.entity, grant.project.entity)
        image1 = self.useFixture(fixtures.Image(federated))
        image2 = self.useFixture(fixtures.Image(federated))
        openstack = base.OpenStackClient()
        image3 = self.useFixture(fixtures.Image(openstack))
        # Test filtering
        sentinel = base.SentinelClient()
        images = list(sentinel.image.images.list())
        self.assertEqual(len(images), 2)
        self.assertThat(image1.entity, matchers.IsInCollection(images))
        self.assertThat(image2.entity, matchers.IsInCollection(images))
        self.assertThat(image3.entity, matchers.IsNotInCollection(images))
        # Test limits
        images = list(sentinel.image.images.list(limit=1))
        self.assertEqual(len(images), 1)
        images = list(sentinel.image.images.list(marker=images[0].id, limit=1))
        self.assertEqual(len(images), 1)
        images = list(sentinel.image.images.list(marker=images[0].id, limit=1))
        self.assertEqual(len(images), 0)

# vi: ts=4 et:

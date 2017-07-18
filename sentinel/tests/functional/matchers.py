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

"""Custom matchers for use with testtools assertions"""


class IsInCollectionMismatch(object):
    def __init__(self, resource, collection):
        self.resource = resource
        self.collection = collection
    def describe(self):
        return '{} is not in {}'.format(self.resource, self.collection)
    def get_details(self):
        return {}


class IsInCollection(object):
    def __init__(self, collection):
        self.collection = collection
    def __str__(self):
        return 'IsInCollection({})'.format(self.collection)
    def match(self, actual):
        ids = [x.id for x in self.collection]
        if actual.id not in ids:
            return IsInCollectionMismatch(actual.id, ids)
        return None


class IsNotInCollectionMismatch(object):
    def __init__(self, resource, collection):
        self.resource = resource
        self.collection = collection
    def describe(self):
        return '{} is in {}'.format(self.resource, self.collection)
    def get_details(self):
        return {}


class IsNotInCollection(object):
    def __init__(self, collection):
        self.collection = collection
    def __str__(self):
        return 'IsInCollection({})'.format(self.collection)
    def match(self, actual):
        ids = [x.id for x in self.collection]
        if actual.id in ids:
            return IsNotInCollectionMismatch(actual.id, ids)
        return {}

# vi: ts=4 et:

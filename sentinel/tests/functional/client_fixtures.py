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

import uuid

import fixtures


PREFIX = 'sentinel-test-'


def _get_unique_name():
    return PREFIX + uuid.uuid4().hex


class FixtureBase(fixtures.Fixture):
    def __init__(self, client):
        super(FixtureBase, self).__init__()
        self.client = client
        self.entity = None


class User(FixtureBase):
    def _setUp(self):
        self.entity = self.client.identity.users.create(_get_unique_name())
        self.addCleanup(self.client.identity.users.delete, self.entity)


class Project(FixtureBase):
    def __init__(self, client, parent=None):
        super(Project, self).__init__(client)
        self.parent = parent

    def _setUp(self):
        parent = None
        if self.parent:
            parent = self.parent.entity
        self.entity = self.client.identity.projects.create(
            _get_unique_name(),
            'default',
            parent=parent)
        self.addCleanup(self.client.identity.projects.delete, self.entity)


class Group(FixtureBase):
    def _setUp(self):
        self.entity = self.client.identity.groups.create(_get_unique_name())
        self.addCleanup(self.client.identity.groups.delete, self.entity)


class GroupUser(FixtureBase):
    def _setUp(self):
        self.user = self.useFixture(User(self.client))
        self.group = self.useFixture(Group(self.client))
        self.client.identity.users.add_to_group(self.user.entity, self.group.entity)


class Role(FixtureBase):
    def _setUp(self):
        # SP provides us with a role
        self.entity = self.client.identity.roles.list()[0]


class UserProjectGrant(FixtureBase):
    def _setUp(self):
        self.user = self.useFixture(User(self.client))
        self.project = self.useFixture(Project(self.client))
        self.role = self.useFixture(Role(self.client))
        self.client.identity.roles.grant(
            self.role.entity,
            user=self.user.entity,
            project=self.project.entity)


class GroupProjectGrant(FixtureBase):
    def _setUp(self):
        self.group = self.useFixture(Group(self.client))
        self.project = self.useFixture(Project(self.client))
        self.role = self.useFixture(Role(self.client))
        self.client.identity.roles.grant(
            self.role.entity,
            group=self.group.entity,
            project=self.project.entity)


# vi: ts=4 et:

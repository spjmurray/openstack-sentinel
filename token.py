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

"""
Manages our form of token.

Authentication and authorization are handled via X.509 certificates, but we
still need a some form of token to remember scoping information if an IdP
were to bind to a specific project.

We basically store scoping infomation as the subject token, which is
marshalled into json and then base 64 encoded.  This is then decoded by a
middleware hook so that API requests can be scoped as necessary.
"""

import base64
import json

class Token(object):
    def __init__(self, **kwargs):
        self._project_id = kwargs.get('project_id', None)

    @property
    def project_id(self):
        return self._project_id

    def marshal(self):
        token = {
            'scope': {
                'project': {
                    'id': self._project_id,
                }
            }
        }
        return base64.b64encode(json.dumps(token))

    @staticmethod
    def unmarshal(data):
        token = json.loads(base64.b64decode(data))
        return Token(project_id=token['scope']['project']['id'])


# vi: ts=4 et:

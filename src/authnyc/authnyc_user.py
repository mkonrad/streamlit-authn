# authnyc_user.py 
# Description: A Streamlit authentication demonstration application
# Copyright 2024 Michael Konrad 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Date: 2024-07-02

import persistent
import persistent.list
import uuid

class AuthnycUser(persistent.Persistent):
    def __init__(self, user):
        if user['email'] is None:
            raise RuntimeError("Missing required attribute email address.")
        
        self.id = uuid.uuid4()
        self.name = user['name']
        self.given_name = user['given_name']
        self.family_name = user['family_name']
        self.email = user['email']
        self.phone_number = user['phone_number']
        self.linked_accounts = persistent.list.PersistentList()


    def add_linked_account(self, account):
        self.linked_accounts.append(account)
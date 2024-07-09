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

import uuid


def create_user_record(name, email, sub, given_name, family_name,  
                       phone_number, linked_account):
    """
    Create a new user database record. 

    Args:
        name: required - the full name of the account to be created
        email: required - the email address of the account to be created
        sub: required - the primary identity provider of this account
        given_name: the first name of the account to be created
        family_name: the last name of the account to be created
        phone_number: the phone number of the account to be created
        linked_account: an alternate identity provider account to be linked 
                          to this account
        
        The following metadata will be generated: unique ID (UUIDv4),  
        inserted_at and updated_at  timestamps. 

    Returns: 
        The user record ready to be inserted into the TinyDB user store.
    """
    
    # name and email address are required
    if name is None and email is None and sub is None:
        raise RuntimeError("Name, email address, and identity provider are required attributes.")
    
    # Generate UUID and insert_at timestamp
    


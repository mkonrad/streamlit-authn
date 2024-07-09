# user_utils.py 
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

import common_utils as cu
import date_utils as du
import base64
import json
import os
import uuid
import streamlit as st

from datetime import datetime
from tinydb import TinyDB, Query
from loguru import logger


def initialize_user_store():
    user_store_filename = r'user_store.json'
    user_store_path = os.path.join(os.getcwd(), user_store_filename)

    db = TinyDB(user_store_path)

    if 'user_store' not in st.session_state:
        st.session_state.user_store = db


def finduser(email):
    logger.debug("Searching for user...{}", email)
    if 'user_store' not in st.session_state:
        initialize_user_store()

    user_store = st.session_state.user_store

    User = Query()
    user_record = user_store.search(User.email == email)
    if user_record == []:
        logger.info("User not found, search result...{}", user_record)
        user_record = None
    else:
        logger.debug("User found...{}", user_record[0])
        user_record = dict(user_record[0])

    return user_record


def adduser(id_token):
    # TBD: verify the signature for security
    payload = id_token.split(".")[1] + "=="

    decoded_payload = json.loads(base64.urlsafe_b64decode(payload))
    logger.debug("Payload...{}", decoded_payload)

    if 'email' in decoded_payload:
        email = decoded_payload['email']
        user_record = finduser(email)
        if user_record is None:
            name = ''
            sub = ''
            nickname = ''
            given_name = ''
            family_name = ''
            phone_number = ''
            if 'name' in decoded_payload:
                name = decoded_payload['name']
            if 'sub' in decoded_payload:
                sub = decoded_payload['sub']
            if 'nickname' in decoded_payload:
                nickname = decoded_payload['nickname']
            if 'given_name' in decoded_payload:
                given_name = decoded_payload['given_name']
            if 'family_name' in decoded_payload:
                family_name = decoded_payload['family_name']
            if 'phone_number' in decoded_payload:
                phone_number = decoded_payload['phone_number']

            # Generate UUID and inserted_at timestamp
            id = str(uuid.uuid4())
            date_format = '%Y-%d-%m %H:%M:%S'
            inserted_at = du.convert_date(format=date_format)

            user_record = {
                "id": id,
                "inserted_at": inserted_at,
                "updated_at": inserted_at,
                "name": name,
                "email": email,
                "sub": sub,
                "nickname": nickname,
                "given_name": given_name,
                "family_name": family_name,
                "phone_number": phone_number
            }

            logger.debug("Adding user to user store...{}", user_record)
            user_store = st.session_state.user_store
            user_store.insert(user_record)

        return user_record
    
    else:
        raise RuntimeError("Missing required attribute email.")
        
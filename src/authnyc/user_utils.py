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

import date_utils as du
import base64
import json
import os
import uuid
import streamlit as st

from auth_utils import initialize_auth0_api_authenticator
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

    user_record = get_payload_data(payload)

    if 'email' in user_record:
        email = user_record['email']
        found_record = finduser(email)
        if found_record is None:
            # Generate UUID and inserted_at timestamp
            id = str(uuid.uuid4())
            date_format = '%Y-%d-%m %H:%M:%S'
            inserted_at = du.convert_date(format=date_format)

            user_record['id'] = id
            user_record['inserted_at'] = inserted_at
            user_record['updated_at'] = inserted_at
        
            logger.debug("Adding user to user store...{}", user_record)
            user_store = st.session_state.user_store
            user_store.insert(user_record)
        else:
            # Update existing record with any changes from OIDC
            user_record = update_local_user_record(user_record, found_record)

        return user_record
    
    else:
        raise RuntimeError("Missing required attribute email.")
        
def login():
    if 'authenticator' in st.session_state:
        authenticator = st.session_state.authenticator
        redirect_uri = st.session_state.redirect_uri
        config = st.session_state.config

        if 'token' not in st.session_state:
            result = authenticator.authorize_button(
                name='Log in with Auth0',
                icon='https://cdn.auth0.com/quantum-assets/dist/latest/favicons/auth0-favicon-onlight.png',
                redirect_uri=redirect_uri,
                scope="openid email profile",
                key='auth0_login_btn',
                extras_params={"prompt": "consent", "access_type": "offline"}
            )

            if result and 'token' in result:
                logger.debug("Authentication result...{}", result)
                #token = result['token']['access_token']
                token = result['token']

                # Verify JWT
                # Algorithm provided in header throws "InvalidAlgorithmError"
                #token_header_data = jwt.get_unverified_header(token)
                #logger.debug("Token header data...{}", token_header_data)

                #jwt.decode(jwt=token, key=config['CLIENT_SECRET'], 
                #           algorithms=["RS256", ])
                
                st.session_state.token = token
                verify_authentication()
                st.rerun()
    

def verify_authentication():
    if 'token' in st.session_state:       
        id_token = st.session_state.token["id_token"]  
        user_record = adduser(id_token)

        if 'user_record' not in st.session_state:
            st.session_state.user_record = user_record

        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = True


def update_auth0_user(updated_user_record):
    auth0_mgmt_api = initialize_auth0_api_authenticator()
    id = updated_user_record['sub']
    del updated_user_record['sub']
    result = auth0_mgmt_api.users.update(id, updated_user_record)
    logger.debug(result)


def get_payload_data(payload):
    decoded_payload = json.loads(base64.urlsafe_b64decode(payload))
    logger.debug("Payload...{}", decoded_payload)

    sub = ''
    name = ''
    nickname = ''
    given_name = ''
    family_name = ''
    email = ''
    phone_number = ''
    amr = []
    if 'sub' in decoded_payload:
        sub = decoded_payload['sub']
    if 'name' in decoded_payload:
        name = decoded_payload['name']
    if 'nickname' in decoded_payload:
        nickname = decoded_payload['nickname']
    if 'given_name' in decoded_payload:
        given_name = decoded_payload['given_name']
    if 'family_name' in decoded_payload:
        family_name = decoded_payload['family_name']
    if 'email' in decoded_payload:
        email = decoded_payload['email']
    if 'phone_number' in decoded_payload:
        phone_number = decoded_payload['phone_number']
    if 'amr' in decoded_payload:
        amr = decoded_payload['amr']

    user_record = {
        "sub": sub,
        "name": name,
        "nickname": nickname,
        "given_name": given_name,
        "family_name": family_name,
        "email": email,
        "phone_number": phone_number,
        "amr": amr
    }

    return user_record


def update_local_user_record(user_record, found_record):
    user_store = st.session_state.user_store
    
    email = found_record['email']
    id = found_record['id']
    inserted_at = found_record['inserted_at']

    date_format = '%Y-%m-%d %H:%M:%S'
    updated_at = du.convert_date(format=date_format)

    user_record['id'] = id
    user_record['inserted_at'] = inserted_at
    user_record['updated_at'] = updated_at

    User = Query()
    user_store.update(user_record, User.email == email)
    logger.debug("User store updated...{}", user_store.all())
    return user_record
# oidc_utils.py 
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
# Date: 2024-07-19

import os
import requests
import streamlit as st
import validators

from loguru import logger
from tinydb import TinyDB, Query

def initialize_oidc_store():
    oidc_store_filename = r'oidc_store.json'
    oidc_store_path = os.path.join(os.getcwd(), oidc_store_filename)

    db = TinyDB(oidc_store_path)

    if 'oidc_store' not in st.session_state:
        st.session_state.oidc_store = db


def parse_oidc_disc_url():
    if 'oidc_disc_url' not in st.session_state:
        logger.error("Missing OIDC Discovery URL.")
    else:
        if validate_form_values():
            get_oidc_configuration()


def validate_form_values():
    disc_url = st.session_state['oidc_disc_url']
    client_id = st.session_state['oidc_client_id']
    client_secret = st.session_state['oidc_client_secret']
    disc_url_valid = validators.url(disc_url)
    if client_id is not None and client_secret is not None and disc_url_valid:
        return True
    
    return False


def get_oidc_configuration():
    response = requests.get(st.session_state['oidc_disc_url'])
    logger.debug("OIDC configuration response...{}", response.json())
    '''
    {'issuer': 'https://dev-skci602t6y4tt6zi.us.auth0.com/', 
    'authorization_endpoint': 'https://dev-skci602t6y4tt6zi.us.auth0.com/authorize', 
    'token_endpoint': 'https://dev-skci602t6y4tt6zi.us.auth0.com/oauth/token', 
    'device_authorization_endpoint': 'https://dev-skci602t6y4tt6zi.us.auth0.com/oauth/device/code', 
    'userinfo_endpoint': 'https://dev-skci602t6y4tt6zi.us.auth0.com/userinfo', 'mfa_challenge_endpoint': 
    'https://dev-skci602t6y4tt6zi.us.auth0.com/mfa/challenge', 
    'jwks_uri': 'https://dev-skci602t6y4tt6zi.us.auth0.com/.well-known/jwks.json', 'registration_endpoint': 'https://dev-skci602t6y4tt6zi.us.auth0.com/oidc/register', 'revocation_endpoint': 'https://dev-skci602t6y4tt6zi.us.auth0.com/oauth/revoke', 'scopes_supported': ['openid', 'profile', 'offline_access', 'name', 'given_name', 'family_name', 'nickname', 'email', 'email_verified', 'picture', 'created_at', 'identities', 'phone', 'address'], 'response_types_supported': ['code', 'token', 'id_token', 'code token', 'code id_token', 'token id_token', 'code token id_token'], 'code_challenge_methods_supported': ['S256', 'plain'], 'response_modes_supported': ['query', 'fragment', 'form_post'], 'subject_types_supported': ['public'], 'id_token_signing_alg_values_supported': ['HS256', 'RS256', 'PS256'], 'token_endpoint_auth_methods_supported': ['client_secret_basic', 'client_secret_post', 'private_key_jwt'], 'claims_supported': ['aud', 'auth_time', 'created_at', 'email', 'email_verified', 'exp', 'family_name', 'given_name', 'iat', 'identities', 'iss', 'name', 'nickname', 'phone_number', 'picture', 'sub'], 'request_uri_parameter_supported': False, 'request_parameter_supported': False, 'token_endpoint_auth_signing_alg_values_supported': ['RS256', 'RS384', 'PS256'], 'end_session_endpoint': 'https://dev-skci602t6y4tt6zi.us.auth0.com/oidc/logout'}
    '''
    oidc_dict = response.json()
    oidc_dict['client_id'] = st.session_state['oidc_client_id']
    oidc_dict['client_secret'] = st.session_state['oidc_client_secret']

    logger.debug("OIDC client configuration...{}", oidc_dict)


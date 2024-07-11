# auth_utils.py 
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
# Date: 2024-06-19

import os
import streamlit as st
import streamlit_authenticator as stauth
import yaml

from auth0.authentication import GetToken
from auth0.management import Auth0
from common_utils import app_dir
from loguru import logger
from streamlit_oauth import OAuth2Component
from yaml.loader import SafeLoader

def initialize_creds_authenticator():
    wd = app_dir()
    config_file = r'creds_authenticator.yaml'
    auth_config_path = os.path.join(wd, config_file)

    with open(auth_config_path) as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['pre-authorized']
    )

    return authenticator


def confirm_creds(authenticator):
    name, authentication_status, username = authenticator.login()

    if st.session_state["authentication_status"]:
        authenticator.logout(location='sidebar')
        st.write(f'Welcome *{st.session_state["name"]}*')
        st.title('Bringing some :sun_with_face:')
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')


def initialize_token_authenticator():
    # Coniugration is initialized in common_utils.py 
    if st.session_state.config:
        config = st.session_state.config
        AUTHORIZE_URL = config['AUTHORIZE_URL']
        TOKEN_URL = config['TOKEN_URL']
        REFRESH_TOKEN_URL = config['REFRESH_TOKEN_URL']
        REVOKE_TOKEN_URL = config['REVOKE_TOKEN_URL']
        CLIENT_ID = config['CLIENT_ID']
        CLIENT_SECRET = config['CLIENT_SECRET']

        if 'redirect_uri' not in st.session_state:
            st.session_state.redirect_uri = config['REDIRECT_URI']

        authenticator = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_URL, 
                                        TOKEN_URL, REFRESH_TOKEN_URL, REVOKE_TOKEN_URL)
        
        if 'authenticator' not in st.session_state:
            st.session_state.authenticator = authenticator

    else:
        st.error('OAuth settings not found.', icon=":material/error:")

    return None
 

def initialize_auth0_api_authenticator():
    # Coniugration is initialized in common_utils.py 
    if st.session_state.api_config:
        api_config = st.session_state.api_config

        if 'API_DOMAIN' in api_config:
            API_DOMAIN = api_config['API_DOMAIN']
        if 'API_CLIENT_ID' in api_config:
            API_CLIENT_ID = api_config['API_CLIENT_ID']
        if 'API_CLIENT_SECRET' in api_config:
            API_CLIENT_SECRET = api_config['API_CLIENT_SECRET']
        if 'API_AUDIENCE' in api_config:
            API_AUDIENCE = api_config['API_AUDIENCE']

        get_token = GetToken(API_DOMAIN, API_CLIENT_ID, 
                             client_secret=API_CLIENT_SECRET)
        token = get_token.client_credentials(API_AUDIENCE.format(API_DOMAIN))
        mgmt_api_token = token['access_token']
        
        auth0 = Auth0(API_DOMAIN, mgmt_api_token)

        return auth0
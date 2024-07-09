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

import user_utils as uu
import common_utils as cu
import os
import streamlit as st
import streamlit_authenticator as stauth
import yaml

from loguru import logger
from streamlit_oauth import OAuth2Component, StreamlitOauthError
from yaml.loader import SafeLoader

def initialize_creds_authenticator():
    wd = cu.app_dir()
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
 

def login():
    if 'authenticator' in st.session_state:
        authenticator = st.session_state.authenticator
        redirect_uri = st.session_state.redirect_uri

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
                st.session_state.token = result.get('token')
                verify_authentication()
                st.rerun()
    

def verify_authentication():
    if 'token' in st.session_state:
        #result = st.session_state.auth_result
        #del st.session_state.auth_result
               
        id_token = st.session_state.token["id_token"]  
        user_record = uu.adduser(id_token)

        if 'user_record' not in st.session_state:
            st.session_state.user_record = user_record

        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = True
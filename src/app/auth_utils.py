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

import common_utils as cu
import base64
import json
import os
import streamlit as st
import streamlit_authenticator as stauth
import yaml

from dotenv import load_dotenv
from flask import redirect
from streamlit.logger import get_logger
from streamlit_oauth import OAuth2Component
from urllib.parse import quote_plus, urlencode
from yaml.loader import SafeLoader

logger = get_logger(__name__)

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


def confirm_creds_session(authenticator):
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

        return OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_URL, 
                               TOKEN_URL, REFRESH_TOKEN_URL, REVOKE_TOKEN_URL)
    else:
        st.error('OAuth settings not found.', icon=":material/error:")

    return None
    


def logout_button_clicked():
    st.session_state.logout = True
    logout()
        

def logout():
    if st.session_state.config:
        config = st.session_state.config
        LOGOUT_URL = config['LOGOUT_URL']
        CLIENT_ID = config['CLIENT_ID']
        
    if st.session_state.token:
        ID_TOKEN = st.session_state.token['id_token']
    if st.session_state.logout:
        if 'first_name' in st.session_state:
            del st.session_state.first_name
        if 'last_name' in st.session_state:
            del st.session_state.last_name
        if 'auth_email' in st.session_state:
            del st.session_state.auth_email
        del st.session_state.token

        logger.info("Calling redirect...")
        return redirect(LOGOUT_URL + "?" + urlencode(
            {
                "returnTo": 'http://localhost:8051',
                "client_id": CLIENT_ID,
                "id_token_hint": ID_TOKEN
            },
            quote_via=quote_plus,
            )
        )

    

def confirm_token_session(authenticator):
    if authenticator is not None:
        if 'auth_email' not in st.session_state:
            with st.sidebar:
                result = authenticator.authorize_button(
                    name='Log in with Auth0',
                    icon='https://cdn.auth0.com/quantum-assets/dist/latest/favicons/auth0-favicon-onlight.png',
                    redirect_uri='http://localhost:8501',
                    scope="openid email profile",
                    key='auth0_btn',
                    extras_params={"prompt": "consent", "access_type": "offline"},
                    use_container_width=False,
                    pkce='S256',
                )
                

            if result:
                st.write(result)
                # decode the id_token jwt and get the user's email address
                id_token = result["token"]["id_token"]
                # verify the signature is an optional step for security
                payload = id_token.split(".")[1]
                # add padding to the payload if needed
                payload += "=" * (-len(payload) % 4)
                payload = json.loads(base64.b64decode(payload))
                st.write(f'Payload...*{payload}*')
                if 'email' in payload:
                    auth_email = payload['email']
                    if 'auth_email' not in st.session_state:
                        st.session_state['auth_email'] = auth_email
                if 'nickname' in payload:
                    nickname = payload['nickname']
                    if 'nickname' not in st.session_state:
                        st.session_state.nickname = nickname
                if 'given_name' in payload:
                    first_name = payload['given_name']
                    if 'first_name' not in st.session_state:
                        st.session_state['first_name'] = first_name
                if 'family_name' in payload:
                    last_name = payload['family_name']
                    if 'last_name' not in st.session_state:
                        st.session_state['last_name'] = last_name 
                if 'token' not in st.session_state:
                    st.session_state['token'] = result['token']
                st.rerun()

        else:
            if 'first_name' in st.session_state and 'last_name' in st.session_state:
                st.write(f'Welcome *{st.session_state["first_name"]}* *{st.session_state["last_name"]}*')
            st.write('Bringing some :sun_with_face:')
            st.write(st.session_state['auth_email'])
            st.write(st.session_state['token'])
            with st.sidebar:
                st.button("Log out", on_click=logout_button_clicked)

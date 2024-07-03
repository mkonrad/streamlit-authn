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

import authnyc_user as au
import user_utils as uu
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

        return OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_URL, 
                               TOKEN_URL, REFRESH_TOKEN_URL, REVOKE_TOKEN_URL)
    else:
        st.error('OAuth settings not found.', icon=":material/error:")

    return None
 

def confirm_token(authenticator):
    if authenticator is not None:
        if 'authnyc_user' not in st.session_state:
            with st.sidebar:
                result = authenticator.authorize_button(
                    name='Log in with Auth0',
                    icon='https://cdn.auth0.com/quantum-assets/dist/latest/favicons/auth0-favicon-onlight.png',
                    redirect_uri='http://localhost:8501',
                    scope="openid email profile",
                    key='auth0_btn',
                    extras_params={"prompt": "consent", "access_type": "offline"},
                    use_container_width=False
                )
                

            if result:
                st.write(result)
                # decode the id_token jwt and get the user's email address
                id_token = result["token"]["id_token"]
                # verify the signature is an optional step for security
                payload = id_token.split(".")[1]
                decoded_payload = json.loads(base64.urlsafe_b64decode(payload))
                st.write(f'Payload...*{decoded_payload}*')
                if 'email' in decoded_payload:
                    email = decoded_payload['email']
                    authnyc_user = uu.finduser(email)
                    if authnyc_user is None:
                        name = ''
                        nickname = ''
                        given_name = ''
                        family_name = ''
                        phone_number = ''
                        if 'name' in decoded_payload:
                            name = decoded_payload['name']
                        if 'nickname' in decoded_payload:
                            nickname = decoded_payload['nickname']
                        if 'given_name' in decoded_payload:
                            given_name = decoded_payload['given_name']
                        if 'family_name' in decoded_payload:
                            family_name = decoded_payload['family_name']
                        if 'phone_number' in decoded_payload:
                            phone_number = decoded_payload['phone_number']

                        authnyc_user = au.AuthnycUser({
                            "name": name,
                            "nickname": nickname,
                            "given_name": given_name,
                            "family_name": family_name,
                            "phone_number": phone_number,
                            "email": email
                        })

                        uu.adduser(authnyc_user)

                    if 'authnyc_user' not in st.session_state:
                        st.session_state.authnyc_user = authnyc_user
                
                    if 'token' not in st.session_state:
                        st.session_state['token'] = result['token']
                st.rerun()

        else:
            if 'authnyc_user' in st.session_state:
                st.write(f'Welcome *{st.session_state.authnyc_user.name}*')
            st.write('Bringing some :sun_with_face:')
            st.write(st.session_state.authnyc_user.email)
            st.write(st.session_state['token'])
            with st.sidebar:
                st.button("Log out", on_click=logout_button_clicked)


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
        if 'authnyc_user' in st.session_state:
            del st.session_state.authnyc_user
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
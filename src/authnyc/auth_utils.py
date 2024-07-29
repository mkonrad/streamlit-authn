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

import oidc_utils as oidc
import os
import streamlit as st
import streamlit_authenticator as stauth
import yaml

from auth0.authentication import GetToken
from auth0.management import Auth0
from common_utils import app_path, get_configuration, is_configured
from flask import redirect
from loguru import logger
from streamlit_oauth import OAuth2Component
from urllib.parse import quote_plus, urlencode
from user_utils import adduser
from yaml.loader import SafeLoader

def initialize_creds_authenticator():
    config_file = r'creds_authenticator.yaml'
    auth_config_path = os.path.join(app_path(), config_file)

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


@st.cache_resource
def get_token_authenticator(provider_key):
    oidc_config = oidc.get_provider_config(provider_key)
    #logger.debug("Initialize token oidc provider...{}", oidc_config)

    provider = oidc_config['config']['provider']
    client = oidc_config['config']['client']

    authenticator = OAuth2Component(client['client_id'], client['client_secret'], 
                                    provider['authorization_endpoint'],
                                    provider['token_endpoint'],
                                    provider['token_endpoint'],
                                    provider['revocation_endpoint'])
    
    return authenticator
 

@st.cache_resource
def get_auth0_api_authenticator():
    if is_configured():
        app_config = get_configuration()
        api_config = oidc.get_provider_config(app_config['oidc_api_provider_key'])
        #logger.debug("Get Auth0 API authenticator - state...{}", api_config)

        api_provider = api_config['config']['provider']
        api_domain = api_provider['api_domain']
        api_client_id = api_provider['api_client_id']
        api_client_secret = api_provider['api_client_secret']
        api_audience = api_provider['api_audience']

        get_token = GetToken(api_domain, api_client_id, 
                                client_secret=api_client_secret)
        token = get_token.client_credentials(api_audience.format(api_domain))
        mgmt_api_token = token['access_token']
        
        return Auth0(api_domain, mgmt_api_token)


def login():
    if is_configured():
        app_config = get_configuration()
        authenticator = get_token_authenticator(app_config['oidc_provider_key'])
        logger.debug("Login state...{}", st.session_state)
        redirect_uri = app_config['redirect_uri']

        if 'token' not in st.session_state:
            result = authenticator.authorize_button(
                name='Log in with Auth0',
                icon='https://cdn.auth0.com/quantum-assets/dist/latest/favicons/auth0-favicon-onlight.png',
                redirect_uri=redirect_uri,
                scope="openid email profile",
                key='authenticator_login',
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
                
                st.session_state['token'] = token
                verify_authentication()
                st.rerun()


def logout():
    if is_configured():
        app_config = get_configuration()
        client_id = app_config['oidc_client_id']
        logout_endpoint = app_config['logout_endpoint']
        redirect_uri = app_config['redirect_uri']
            
        if st.session_state['token']:
            id_token = st.session_state['token']['id_token']
        if st.session_state['logout']:
            del st.session_state['user_record']
            del st.session_state['token']
            del st.session_state['logout']
            del st.session_state['authenticated']

            logger.info("Calling redirect...{}", logout_endpoint)
            return redirect(logout_endpoint + "?" + urlencode(
                {
                    "returnTo": redirect_uri,
                    "client_id": client_id,
                    "id_token_hint": id_token
                },
                quote_via=quote_plus,
                )
            )
    

def verify_authentication():
    if 'token' in st.session_state:       
        id_token = st.session_state.token['id_token']  
        user_record = adduser(id_token)

        if 'user_record' not in st.session_state:
            st.session_state['user_record'] = user_record

        if 'authenticated' not in st.session_state:
            st.session_state['authenticated'] = True
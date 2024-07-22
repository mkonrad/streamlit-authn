# authnyc_form.py 
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

import oidc_utils as oidc
import streamlit as st

from auth_utils import initialize_token_authenticator
from loguru import logger


def present_oidc_discovery_form():
    with st.form(key='oidc_discovery_form'):
        provider_list = ["Select a provider", "Auth0"]
        st.selectbox('OIDC Provider', provider_list, index = 0,  
                     key='selected_oidc_provider')
        st.text_input(label="Enter OIDC Discovery URL",
                      max_chars=128, key='oidc_discovery_url')
        st.text_input(label="Enter Client ID",
                      max_chars=128, key='oidc_client_id')
        st.text_input(label="Enter Client Secret",
                      max_chars=128, key='oidc_client_secret',
                      type='password')
        st.text_input(label="Enter Redirect URI",
                      max_chars=128, key='redirect_uri',
                      placeholder="http://localhost:8501")
        
        st.form_submit_button("Next", 
                              on_click=oidc_discovery_form_clicked)


def present_oidc_api_form():
    valid = oidc.validate_oidc_discovery_form()
    if valid:
        del st.session_state['oidc_discovery_form_submitted']
        with st.form(key='oidc_api_form'):
            api_provider_list = ["Select an API", "Auth0 API"]
            st.selectbox('OIDC API', api_provider_list, index = 0,  
                     key='selected_oidc_api_provider')
            st.text_input(label="Enter API Domain", max_chars=128, 
                          key='api_domain')
            st.text_input(label="Enter API Client ID", max_chars=128, 
                          key='api_client_id')
            st.text_input(label="Enter API Client Secret", max_chars=128, 
                          key='api_client_secret', type='password')
            st.text_input(label="Enter API Audience", max_chars=128, 
                          key='api_audience')
            
            st.form_submit_button("Next", on_click=oidc_api_form_clicked)
    else:
        del st.session_state['oidc_discovery_form_submitted']


def present_authnyc_form():
    valid = oidc.validate_oidc_api_form()
    if valid:
        del st.session_state['oidc_api_form_submitted']
        oidc_config = oidc.get_oidc_provider_config()
        if 'authenticated' not in st.session_state:
            initialize_token_authenticator(oidc_config)

        if 'authenticated' in st.session_state:
            st.write(f'Welcome *{st.session_state.user_record['name']}*')
            st.write('Bringing some :sun_with_face:')
            st.write(st.session_state['token'])
    else:
        del st.session_state['oidc_api_form_submitted']
            

def oidc_discovery_form_clicked():
    if 'oidc_discovery_form_submitted' not in st.session_state:
        st.session_state['oidc_discovery_form_submitted'] = True

    logger.debug("OIDC Discovery form state...{}", st.session_state)


def oidc_api_form_clicked():
    if 'oidc_api_form_submitted' not in st.session_state:
        st.session_state['oidc_api_form_submitted'] = True

    logger.debug("OIDC API form state...{}", st.session_state)
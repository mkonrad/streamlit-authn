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
        st.selectbox('OIDC Provider', st.session_state['oidc_provider_names'], 
                     index = 0, key='selected_oidc_provider')
        st.text_input(label="Enter OIDC Discovery URL",
                      max_chars=128, key='oidc_discovery_url',
                      placeholder="https://oidc.provider.domain/.well-known/openid-configuration")
        st.text_input(label="Client ID",
                      max_chars=128, key='oidc_client_id',
                      placeholder="abx...czy")
        st.text_input(label="Client Secret",
                      max_chars=128, key='oidc_client_secret',
                      type='password',
                      placeholder="***...***")
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
            st.selectbox('OIDC API', st.session_state['oidc_api_provider_names'], 
                         index = 0, key='selected_oidc_api_provider')
            st.text_input(label="API Domain", max_chars=128, 
                          key='api_domain',
                          placeholder="api.resource.domain")
            st.text_input(label="API Client ID", max_chars=128, 
                          key='api_client_id',
                          placeholder="czy...abx")
            st.text_input(label="API Client Secret", max_chars=128, 
                          key='api_client_secret', type='password',
                          placeholder="***...***")
            st.text_input(label="API Audience", max_chars=128, 
                          key='api_audience',
                          placeholder="https://api.provider.domain/api/v2/")
            
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
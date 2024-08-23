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

from loguru import logger


# Workflow form for capturing OIDC Provider details
def present_oidc_discovery_form():
    with st.form(key='oidc_discovery_form'):
        st.selectbox('OIDC Provider', oidc.get_oidc_provider_names(), 
                     index = 0, key='selected_oidc_provider')
        st.text_input(label="OIDC Discovery URL",
                      max_chars=128, key='oidc_discovery_url',
                      placeholder="https://oidc.provider.domain/.well-known/openid-configuration")
        st.text_input(label="Client ID",
                      max_chars=128, key='oidc_client_id',
                      placeholder="abx...czy")
        st.text_input(label="Client Secret",
                      max_chars=128, key='oidc_client_secret',
                      type='password',
                      placeholder="***...***")
        st.text_input(label="Redirect URI",
                      max_chars=128, key='oidc_redirect_uri',
                      placeholder="http://localhost:8501",
                      value="http://localhost:8501")
        
        st.form_submit_button("Next", 
                              on_click=oidc_discovery_form_clicked)


# Workflow form for capturing OIDC API Provider details
def present_oidc_api_form():
    del st.session_state['oidc_discovery_form_submitted']
    with st.form(key='oidc_api_form'):
        st.selectbox('OIDC API', oidc.get_oidc_api_provider_names(), 
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


# Authnyc Main page
def present_authnyc():
    #if 'oidc_api_form_submitted' in st.session_state:
    #    del st.session_state['oidc_api_form_submitted']

    if 'authenticated' not in st.session_state or \
        st.session_state['authenticated'] == False:
        st.write("Please log in!")
        
    if 'authenticated' in st.session_state and \
        st.session_state['authenticated'] == True:
        st.write(f'Welcome *{st.session_state['user_record']['name']}*')
        st.write('Bringing some :sun_with_face:')
        st.write(st.session_state['token'])


def oidc_discovery_form_clicked():
    valid = oidc.validate_oidc_discovery_form()
    if valid:
        if 'oidc_discovery_form_submitted' not in st.session_state:
            st.session_state['oidc_discovery_form_submitted'] = True


def oidc_api_form_clicked():
    valid = oidc.validate_oidc_api_form()
    if valid:
        if 'oidc_api_form_submitted' not in st.session_state:
            st.session_state['oidc_api_form_submitted'] = True
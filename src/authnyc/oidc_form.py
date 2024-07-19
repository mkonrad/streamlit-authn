# oidc_form.py 
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


def present_discovery_form():
    oidc_disc_form_btn_label = "Next"
    with st.form(key="oidc_discovery_form"):
        st.text_input(label="Enter Auth0 Discovery URL",
                      max_chars=255, key="oidc_disc_url")
        st.text_input(label="Enter Client ID",
                      max_chars=200, key='oidc_client_id')
        st.text_input(label="Enter Client Secret",
                      max_chars=200, key='oidc_client_secret',
                      type="password")
        
        st.form_submit_button(oidc_disc_form_btn_label, 
                              on_click=oidc_discovery_url_clicked)


def present_api_form():
    oidc.parse_oidc_disc_url()

def oidc_discovery_url_clicked():
    if 'oidc_disc_url_set' not in st.session_state:
        st.session_state.oidc_disc_url_set = True
    logger.debug("OIDC session state...{}", st.session_state)
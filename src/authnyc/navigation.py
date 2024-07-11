# navigation.py 
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
# Date: 2024-07-05
# This code is modified from streamlit-login example:
#   https://github.com/blackary/streamlit-login

import streamlit as st

from flask import redirect
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages
from urllib.parse import quote_plus, urlencode
from user_utils import login
from loguru import logger

def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Unable to get script context.")
    
    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]


def make_sidebar():
    with st.sidebar:
        st.title("Auth:red[n]:orange[y]:blue[c]!")
        st.write()
        st.write()

        login()

        if st.session_state.get("authenticated", False):
            logger.debug("Authenticated user in session state...{}", st.session_state.user_record)
            st.page_link("authnyc.py", label = "Home", icon=":material/home:")
            st.page_link("pages/my_profile.py", label = "My Profile", 
                         icon=":material/manage_accounts:")
            st.button(":arrow_right: Log out", on_click=logout_button_clicked)

        elif get_current_page_name() != "authnyc":
            st.switch_page("authnyc.py")


def logout_button_clicked():
    st.session_state.logout = True
    logout()
        

def logout():
    if st.session_state.config:
        config = st.session_state.config
        LOGOUT_URL = config['LOGOUT_URL']
        CLIENT_ID = config['CLIENT_ID']
        REDIRECT_URI = config['REDIRECT_URI']
        
    if st.session_state.token:
        ID_TOKEN = st.session_state.token['id_token']
    if st.session_state.logout:
        del st.session_state.authenticator
        del st.session_state.user_record
        del st.session_state.authenticated
        del st.session_state.token

        logger.info("Calling redirect...{}", LOGOUT_URL)
        return redirect(LOGOUT_URL + "?" + urlencode(
            {
                "returnTo": REDIRECT_URI,
                "client_id": CLIENT_ID,
                "id_token_hint": ID_TOKEN
            },
            quote_via=quote_plus,
            )
        )
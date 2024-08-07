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

from auth_utils import login, logout
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages
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

        if 'authenticated' in st.session_state and \
            st.session_state['authenticated']:
            #logger.debug("Authenticated user in session state...{}", st.session_state['user_record'])
            st.page_link("authnyc.py", label = "Home", icon=":material/home:")
            st.page_link("pages/myprofile.py", label = "My Profile", 
                         icon=":material/manage_accounts:")
            st.button(":arrow_right: Log out", on_click=logout_button_clicked)

        elif get_current_page_name() != "authnyc":
            st.switch_page("authnyc.py")


def logout_button_clicked():
    st.session_state['logout'] = True
    logout()
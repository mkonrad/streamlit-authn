# app.py 
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

import auth_utils as au
import common_utils as cu
import streamlit as st

from streamlit.logger import get_logger

logger = get_logger(__name__)
logo = cu.get_png_logo()

st.set_page_config(
    page_title="Authnyc",
    page_icon=logo,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': cu.get_help_url()
    }
)

def main(msg):
    st.logo(logo)
    st.header('Welcome to Auth:red[n]:orange[y]:blue[c]!')
    st.write('A Streamlit authentication demonstration application.')
    st.write(msg)
    if st.session_state.valid_oidc:
        authenticator = au.initialize_token_authenticator()
        au.confirm_token_session(authenticator)


if __name__ == "__main__":
    msg = "OIDC configured successfully."
    if 'valid_oidc' not in st.session_state:
        st.session_state.valid_oidc = True
    try: 
        cu.initialize()
    except RuntimeError as e:
        msg = str(e)
        st.session_state.valid_oidc = False

    main(msg)

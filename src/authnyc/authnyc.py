# authnyc.py 
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

import oidc_form as po
import streamlit as st

from common_utils import initialize
from auth_utils import initialize_token_authenticator
from navigation import make_sidebar

def main(msg):
    make_sidebar()
    
    st.header('Welcome to Auth:red[n]:orange[y]:blue[c]!')
    if 'authenticated' not in st.session_state:
        st.write('A Streamlit authentication demonstration application.')

        po.present_discovery_form()
        if 'oidc_disc_url_set' in st.session_state:
            po.present_api_form()

        if st.session_state.valid_oidc == False:
            st.write(f'Status: :red[{msg}]')
        else:
            st.write(f'Status: :green[{msg}]')

    if 'authenticated' in st.session_state:
        st.write(f'Welcome *{st.session_state.user_record['name']}*')
        st.write('Bringing some :sun_with_face:')
        st.write(st.session_state['token'])


if __name__ == "__main__":
    msg = "OIDC configured successfully!"
    
    try: 
        initialize()
        initialize_token_authenticator()
        if 'valid_oidc' not in st.session_state:
            st.session_state.valid_oidc = True
    except RuntimeError as e:
        msg = str(e)
        st.session_state.valid_oidc = False

    main(msg)
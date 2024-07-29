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

import authnyc_form as af
import streamlit as st

from common_utils import initialize, is_configured
from loguru import logger
from navigation import make_sidebar

def main():
    make_sidebar()
    
    st.header('Welcome to Auth:red[n]:orange[y]:blue[c]!')
    if is_configured():
        af.present_authnyc()
    else:
        if 'oidc_discovery_form_submitted' not in st.session_state:
            #logger.debug("Initial OIDC provider state...{}", st.session_state)
            af.present_oidc_discovery_form()
        if 'oidc_discovery_form_submitted' in st.session_state and \
            st.session_state['oidc_discovery_form_submitted'] == True:
            #logger.debug("OIDC provider form submitted - state...{}", st.session_state)
            af.present_oidc_api_form()


if __name__ == "__main__":
    initialize()
        
    main()
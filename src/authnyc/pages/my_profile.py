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
# Date: 2024-07-05

import authnyc.edit_profile_form as pe
import streamlit as st

from navigation import make_sidebar

make_sidebar()

if 'FormSubmitter:user_profile-Edit' in st.session_state and \
    st.session_state['FormSubmitter:user_profile-Edit'] == True:
    pe.present_profile_form_enabled()
else:
    pe.present_profile_form_disabled()
    
if 'FormSubmitter:user_sensitive_profile-Edit' in st.session_state and \
    st.session_state['FormSubmitter:user_sensitive_profile-Edit'] == True:
    pe.present_sensitive_profile_form_enabled()
else:
    pe.present_sensitive_profile_form_disabled()
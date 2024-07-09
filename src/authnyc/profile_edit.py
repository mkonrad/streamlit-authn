# profile_edit.py 
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

import streamlit as st

from loguru import logger

def present_profile_form_disabled():
    if 'user_record' in st.session_state:
        user_record = st.session_state.user_record

        form_button_label="Edit"
        if 'form_button_label' not in st.session_state:
            st.session_state.form_button_label = form_button_label

        with st.form(key="user_profile"):
            st.header("My Profile :standing_person:")
            col1, col2 = st.columns([1,1])
            col1.text_input("**Name**:", value=user_record['name'], 
                            key="profile_form_name", disabled=True)
            col1.text_input("**Nick name**:", value=user_record['nickname'],
                            key="profile_form_nickname", disabled=True)
            col1.text_input("**First name**:", value=user_record['given_name'],
                            key="profile_form_given_name", disabled=True)
            col2.text_input("**Last name**:", value=user_record['family_name'],
                            key="profile_form_family_name", disabled=True)
            col2.text_input("**Email**:", value=user_record['email'],
                            key="profile_form_email", disabled=True)
            col2.text_input("**Phone number**:", value=user_record['phone_number'],
                                key="profile_form_phone_number", disabled=True)
            st.form_submit_button(form_button_label,
                                  on_click=profile_form_button_clicked,
                                  use_container_width=True)
            

def present_profile_form_enabled():
    if 'user_record' in st.session_state:
        user_record = st.session_state.user_record

        form_button_label="Submit"
        if 'form_button_label' not in st.session_state:
            st.session_state.form_button_label = form_button_label

        with st.form(key="user_profile"):
            st.header("My Profile :standing_person:")
            col1, col2 = st.columns([1,1])
            col1.text_input("**Name**:", value=user_record['name'], 
                            key="profile_form_name")
            col1.text_input("**Nick name**:", value=user_record['nickname'],
                            key="profile_form_nickname")
            col1.text_input("**First name**:", value=user_record['given_name'],
                            key="profile_form_given_name")
            col2.text_input("**Last name**:", value=user_record['family_name'],
                            key="profile_form_family_name")
            col2.text_input("**Email**:", value=user_record['email'],
                            key="profile_form_email")
            col2.text_input("**Phone number**:", value=user_record['phone_number'],
                                key="profile_form_phone_number")
            st.form_submit_button(form_button_label, 
                                  on_click=profile_form_button_clicked,
                                  use_container_width=True)
            

def profile_form_button_clicked():
    logger.debug("Profile form button clicked...")
    if 'form_button_label' in st.session_state and \
        st.session_state.form_button_label == 'Edit':
        
        if 'user_record' in st.session_state:
            user_record = st.session_state.user_record

            if user_record['name'] != st.session_state['profile_form_name']:
                user_record['name'] = st.session_state['profile_form_name']
                logger.debug("User record name update...{}", user_record['name'])
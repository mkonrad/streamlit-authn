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

from user_utils import update_auth0_user
from loguru import logger


def present_profile_form_disabled():
    if 'user_record' in st.session_state:
        user_record = st.session_state.user_record

        form_button_label = "Edit"
        with st.form(key="user_profile"):
            st.header("My Profile :standing_person:")
            col1, col2 = st.columns([1,1])
            col1.text_input("**Name**:", value=user_record['name'], 
                            key="profile_form_name", disabled=True)
            col2.text_input("**Nick name**:", value=user_record['nickname'],
                            key="profile_form_nickname", disabled=True)
            col1.text_input("**First name**:", value=user_record['given_name'],
                            key="profile_form_given_name", disabled=True)
            col2.text_input("**Last name**:", value=user_record['family_name'],
                            key="profile_form_family_name", disabled=True)
            st.form_submit_button(form_button_label,
                                  on_click=profile_form_button_clicked,
                                  use_container_width=True)
            

def present_profile_form_enabled():
    if 'user_record' in st.session_state:
        user_record = st.session_state.user_record
        form_button_label = "Submit"
        with st.form(key="user_profile"):
            st.header("My Profile :standing_person:")
            col1, col2 = st.columns([1,1])
            col1.text_input("**Name**:", value=user_record['name'], 
                            key="profile_form_name")
            col2.text_input("**Nick name**:", value=user_record['nickname'],
                            key="profile_form_nickname")
            col1.text_input("**First name**:", value=user_record['given_name'],
                            key="profile_form_given_name")
            col2.text_input("**Last name**:", value=user_record['family_name'],
                            key="profile_form_family_name")
            st.form_submit_button(form_button_label, 
                                  on_click=profile_form_button_clicked,
                                  use_container_width=True)
            

def profile_form_button_clicked():
    logger.debug("Profile form button clicked...")
    if 'FormSubmitter:user_profile-Submit' in st.session_state:
        # updatable user record keys
        user_record_keys = ["name", "nickname", "given_name", "family_name"]
        updated_user_record = compare_user_record(user_record_keys)

        if updated_user_record is not None:
            update_auth0_user(updated_user_record)


def present_sensitive_profile_form_disabled():
    if 'user_record' in st.session_state:
        user_record = st.session_state.user_record
        sensitive_form_button_label = "Edit"
        with st.form(key="user_sensitive_profile"):
            st.caption("Sensitive")
            col1, col2 = st.columns([1,1])
            col1.text_input("**Email**:", value=user_record['email'],
                            key="profile_form_email", type="password", disabled=True)
            col2.text_input("**Phone number**:", value=user_record['phone_number'],
                                key="profile_form_phone_number", type="password", disabled=True)
            st.form_submit_button(sensitive_form_button_label,
                                  on_click=sensitive_profile_form_button_clicked,
                                  use_container_width=True)
            
            
def present_sensitive_profile_form_enabled():
    if 'user_record' in st.session_state:
        user_record = st.session_state.user_record
        sensitive_form_button_label = "Submit"
        with st.form(key="user_sensitive_profile"):
            st.caption("Sensitive")
            col1, col2 = st.columns([1,1])
            col1.text_input("**Email**:", value=user_record['email'],
                            key="profile_form_email")
            col2.text_input("**Phone number**:", value=user_record['phone_number'],
                                key="profile_form_phone_number")
            st.form_submit_button(sensitive_form_button_label,
                                  on_click=sensitive_profile_form_button_clicked,
                                  use_container_width=True)
            

def sensitive_profile_form_button_clicked():
    logger.debug("Sensitive profile form button clicked...")
    if 'FormSubmitter:user_sensitive_profile-Submit' in st.session_state:
        # sensitive updatable user record keys
        user_record_keys = ["email", "phone_number"]
        user_record = compare_user_record(user_record_keys)


def compare_user_record(user_record_keys):
    changed = False
    if 'user_record' in st.session_state:
        user_record = st.session_state.user_record
        paired_keys = profile_form_keys(user_record_keys)

        updated_user_record = {
            "sub": user_record['sub'],
        }

        for key in paired_keys:
            if user_record[key] != st.session_state[paired_keys[key]]:
                updated_user_record[key] = st.session_state[paired_keys[key]]
                logger.debug("Updated user record...{}", updated_user_record)
                changed = True

        if changed:
            return updated_user_record

    return None


def profile_form_keys(user_record_keys):
    """
    Creates a dictionary of keys for comparing information between the 
    user record and the profile edit form.
    
    Args:
        user_record_keys (list): The list of keys from the user record.

    Returns:
        dict: Corresponding key names between the user record and the 
              input fields from the profile edit form. 
    """
    profile_paired_keys = {}

    for key in user_record_keys:
        profile_paired_keys[key] = f'profile_form_{key}'

    return profile_paired_keys
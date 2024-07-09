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

import streamlit as st

from navigation import make_sidebar

make_sidebar()

st.header("My Profile :standing_person:")

if 'user_record' in st.session_state:
    user_record = st.session_state.user_record

    container = st.container(border=True)
    container.write(f'**Name** &nbsp;&nbsp; {user_record['name']}')
    container.write(f'**Nickname** &nbsp;&nbsp; {user_record['nickname']}')
    container.write(f'**First name** &nbsp;&nbsp; {user_record['given_name']}')
    container.write(f'**Last name** &nbsp;&nbsp; {user_record['family_name']}')
    container.write(f'**Email address** &nbsp;&nbsp; {user_record['email']}')
    container.write(f'**Phone number** &nbsp;&nbsp; {user_record['phone_number']}')
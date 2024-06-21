# common_utils.py 
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

import os
import streamlit as st

from dotenv import load_dotenv
from streamlit.logger import get_logger

logger = get_logger(__name__)

def initialize():
    # Load environment variables from .env file
    load_dotenv()

    # Initialize State 
    st.session_state.logout = False


# Utility method to determine where the application is running from.
def app_dir():
    start_path = os.path.realpath(__file__)
    wd = os.path.dirname(start_path)

    return wd

# Utility method to get the application png formatted logo.
def get_png_logo(logo='logo.png'):
    return os.path.join(app_dir(), r'images', logo)


# Utility method to get the application svg formatted logo.
def get_svg_logo(logo='logo.svg'):
    return os.path.join(app_dir(), r'images', logo)


def get_help_url():
    help_url='https://community.auth0.com/'
    return help_url
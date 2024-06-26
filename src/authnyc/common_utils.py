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

import logging
import os
import streamlit as st

from dotenv import dotenv_values

logger = logging.getLogger(__name__)

def initialize():
    config = initialize_config()
    try: 
        if validate_config(config):
            st.session_state.config = config

            # Initialize State 
            st.session_state.logout = False
            return True
    except RuntimeError as e:
        raise e


def initialize_config():
    # Load environment variables from .env file
    env_file = os.path.join(app_dir(), '.env')

    # Load environment to config
    return dotenv_values(env_file)


def validate_config(config):
    """
    Validates all settings have been set.
    
    Args:
        config (dict): The OIDC client configuration settings specified in 
                       .env.

    Returns:
        bool: True if all fields have set values, False otherwise.
    """
    if config is not None:
        keys = list(config.keys())

        try: 
            if validate_keys_list(keys):
                for item in config.values():
                    if item is None:
                        raise RuntimeError("OIDC configuration is missing or incomplete.")
            else:
                return False
            return True
        except RuntimeError as e:
            raise e
        
    return False
    

def validate_keys_list(config_keys):
    """
    Validates the required keys are included in the configuration.

    Args: keys (list): The list of keys to be validated.

    Returns:
        bool: True if the required keys are included, False otherwise.
    """
    oidc_required_settings_file = os.path.join(app_dir(), 
                                               r'oidc-required-settings.txt')
    required_keys = []
    with open(oidc_required_settings_file) as oidc:
        for key in oidc:
            key = key.rstrip('\n')
            required_keys.append(key)

    required_keys.sort()
    config_keys.sort()

    if config_keys == required_keys:
        return True
    
    raise RuntimeError("OIDC configuration is missing or invalid.")


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

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
import tomlkit

from dotenv import dotenv_values
from loguru import logger


config_file = r'authnyc.toml'

def initialize():
    initialize_logger()

    config_path = os.path.join(app_dir(), config_file)
    with open(config_path, "rb") as f:
        authnyc = tomlkit.load(f)

    # Hard coded hack that needs to be updated
    oidc_configured = authnyc['config']['oidc_provider_configured']
    if oidc_configured:
        config = {
            'oidc_provider_name': authnyc['Auth0']['oidc_provider_name'],
            'oidc_api_provider_name': authnyc['Auth0']['oidc_api_provider_name']
        }

        if 'app_config' not in st.session_state:
            st.session_state['app_config'] = config

    if 'oidc_provider_configured' not in st.session_state:
        st.session_state['oidc_provider_configured'] = \
            authnyc['config']['oidc_provider_configured']


def update_configuration():
    doc = tomlkit.document()
    updated_config = tomlkit.table()
    updated_config.add('oidc_provider_configured', st.session_state['oidc_provider_configured'])
    doc.add("config", updated_config)

    if 'selected_oidc_provider' in st.session_state:
        if 'selected_oidc_api_provider' in st.session_state:
            provider_config = tomlkit.table()
            provider_config.add('oidc_provider_name', 
                                st.session_state['selected_oidc_provider'])
            provider_config.add('oidc_api_provider_name', st.session_state['selected_oidc_api_provider'])
            doc.add(tomlkit.nl())
            doc.add(st.session_state['selected_oidc_provider'], provider_config)

    config_path = os.path.join(app_dir(), config_file)
    with open(config_path, "w") as f:
        tomlkit.dump(doc, f)


def initialize_env():
    initialize_logger()
    config = initialize_config()
    try: 
        if validate_config(config):
            st.session_state.config = config

            # Initialize State 
            st.session_state.logout = False
            
            if config['EDIT_PROFILE']:
                api_config = initialize_api_config()
                st.session_state.api_config = api_config

    except RuntimeError as e:
        raise e


def initialize_config():
    # Load environment variables from .env file
    env_file = os.path.join(app_dir(), '.env')

    # Load environment to config
    return dotenv_values(env_file)


def initialize_api_config():
    # Load environment variables from .env file
    env_file = os.path.join(app_dir(), '.apienv')

    # Load environment to config
    return dotenv_values(env_file)


def initialize_logger():
    logname = "authnyc.log"
    log_path = os.path.join(app_dir(), logname)

    logger.add(log_path)


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
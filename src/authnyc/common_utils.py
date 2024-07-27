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

import date_utils as du
import os
import streamlit as st
import sys
import tomlkit
import uuid

from dotenv import dotenv_values
from loguru import logger
from tinydb import TinyDB, Query


config_file = r'authnyc.toml'
config_store = r'config_store.json'

def initialize():
    initialize_logger()

    if is_configured():
        set_state()
    else:
        prep_state()


def is_configured():
    authnyc = get_app_configuration()

    config = authnyc['config']

    if 'oidc_provider_configured' not in st.session_state:
        st.session_state['oidc_provider_configured'] = \
            config['oidc_provider_configured']

    return config['oidc_provider_configured']


def get_app_configuration():
    config_path = os.path.join(app_path(), config_file)
    with open(config_path, "rb") as f:
        authnyc = tomlkit.load(f)

    return authnyc


@st.cache_resource
def get_config_store():
    config_store_path = os.path.join(os.getcwd(), config_store)

    db = TinyDB(config_store_path)

    return db


def store_configuration():
    config_store = get_config_store()

    logger.debug("Store configuration - state...{}", st.session_state)

    id = str(uuid.uuid4())
    date_format = '%Y-%d-%m %H:%M:%S'
    inserted_at = du.convert_date(format=date_format)

    config = {}
    config['name'] = 'authnyc'
    config['id'] = id
    config['inserted_at'] = inserted_at
    config['updated_at'] = inserted_at
    config['oidc_provider_configured'] = \
        st.session_state['oidc_provider_configured']
    config['oidc_provider_key'] = st.session_state['oidc_provider_key']
    config['oidc_api_provider_key'] = st.session_state['oidc_api_provider_key']
    config['redirect_uri'] = st.session_state['redirect_uri']

    config_store.insert(config)


def find_configuration():
    config_store = get_config_store()

    Config = Query()
    config_record = config_store.search(Config.name == 'authnyc')
    if config_record == []:
        logger.info("Application configuration not found.")
        return None
    else:
        config_record = dict(config_record[0])

    return config_record


@st.cache_resource
def set_state():
    config = find_configuration()
    if config is None:
        logger.error("Application configuration not found.")
        sys.exit(1)
    else:
        if 'oidc_provider_configured' not in st.session_state:
            st.session_state['oidc_provider_configured'] = \
                config['oidc_provider_configured']
        if 'oidc_provider_key' not in st.session_state:
            st.session_state['oidc_provider_key'] = config['oidc_provider_key']
        if 'oidc_api_provider_key' not in st.session_state:
            st.session_state['oidc_api_provider_key'] = \
                config['oidc_api_provider_key']
        if 'redirect_uri' not in st.session_state:
            st.session_state['redirect_uri'] = \
                config['redirect_uri']
        
    logger.debug("Set state - session state...{}", st.session_state)
        
    
def prep_state():
    authnyc = get_app_configuration()

    initialize_oidc_providers(authnyc['oidc_providers'].unwrap())
    initialize_oidc_api_providers(authnyc['oidc_api_providers'].unwrap())
        

def update_app_configuration():
    config_path = os.path.join(app_path(), config_file)
    with open(config_path, "r+") as f:
        authnyc = tomlkit.load(f)
        logger.debug("Update app configuration - settings...{}", authnyc)
        logger.debug("Update app configuration - state...{}", st.session_state)
        f.seek(0)
        authnyc['config']['oidc_provider_configured'] =  \
            st.session_state['oidc_provider_configured']

        tomlkit.dump(authnyc, f)

    store_configuration()
        

def initialize_oidc_providers(oidc_providers):
    #logger.debug("Initialization OIDC providers...{}", oidc_providers)
    oidc_provider_names = list(oidc_providers.keys())

    if 'oidc_provider_list' not in st.session_state:
        st.session_state['oidc_provider_list'] = oidc_provider_names

    if 'oidc_providers' not in st.session_state:
        st.session_state['oidc_providers'] = oidc_providers
        

def initialize_oidc_api_providers(oidc_api_providers):
    #logger.debug("Initialization OIDC API providers...{}", oidc_api_providers)
    oidc_api_provider_names = list(oidc_api_providers.keys())

    if 'oidc_api_provider_list' not in st.session_state:
        st.session_state['oidc_api_provider_list'] = oidc_api_provider_names

    if 'oidc_api_providers' not in st.session_state:
        st.session_state['oidc_api_providers'] = oidc_api_providers


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
    env_file = os.path.join(app_path(), '.env')

    # Load environment to config
    return dotenv_values(env_file)


def initialize_api_config():
    # Load environment variables from .env file
    env_file = os.path.join(app_path(), '.apienv')

    # Load environment to config
    return dotenv_values(env_file)


def initialize_logger():
    logname = "authnyc.log"
    log_path = os.path.join(app_path(), logname)

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
    oidc_required_settings_file = os.path.join(app_path(), 
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
def app_path():
    start_path = os.path.realpath(__file__)
    return os.path.dirname(start_path)


# Utility method to get the application png formatted logo.
def get_png_logo(logo='logo.png'):
    return os.path.join(app_path(), r'images', logo)


# Utility method to get the application svg formatted logo.
def get_svg_logo(logo='logo.svg'):
    return os.path.join(app_path(), r'images', logo)


def get_help_url():
    help_url='https://community.auth0.com/'
    return help_url
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


def initialize(log_level):
    logger.info("Initializing application...")
    initialize_logger(log_level)


def initialize_logger(level='DEBUG'):
    logname = "authnyc.log"
    log_path = os.path.join(app_path(), logname)

    logger.add(log_path, level=level)


def is_configured():
    authnyc = get_base_configuration()
    config = authnyc['config']
  
    return config['oidc_provider_configured']


def get_base_configuration():
    config_file = r'authnyc.toml'
    config_path = os.path.join(app_path(), config_file)
    with open(config_path, "rb") as f:
        authnyc = tomlkit.load(f)

    return authnyc


def update_base_configuration():
    config_file = r'authnyc.toml'
    config_path = os.path.join(app_path(), config_file)
    with open(config_path, "r+") as f:
        authnyc = tomlkit.load(f)
        #logger.debug("Update app configuration - settings...{}", authnyc)
        #logger.debug("Update app configuration - state...{}", st.session_state)
        f.seek(0)
        authnyc['config']['oidc_provider_configured'] =  \
            st.session_state['oidc_provider_configured']

        tomlkit.dump(authnyc, f)


def find_configuration():
    config_db = get_config_db()

    Config = Query()
    config_record = config_db.search(Config.name == 'authnyc')
    if config_record == []:
        return None
    else:
        config_record = dict(config_record[0])

    return config_record


@st.cache_resource
def get_configuration():
    config = find_configuration()
    if config is None:
        logger.error("Application configuration not found.")
        sys.exit(1)

    return config


@st.cache_resource
def get_config_db():
    config_db_file = r'config_db.json'
    config_db_path = os.path.join(os.getcwd(), config_db_file)

    db = TinyDB(config_db_path)

    return db


def save_configuration():
    config_db = get_config_db()

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
    config['oidc_client_id'] = st.session_state['client_id']
    config['oidc_provider_key'] = st.session_state['oidc_provider_key']
    config['oidc_api_provider_key'] = st.session_state['oidc_api_provider_key']
    config['redirect_uri'] = st.session_state['redirect_uri']
    config['logout_endpoint'] = st.session_state['logout_endpoint']

    config_db.insert(config)


@st.cache_resource
def get_oidc_providers():
    authnyc = get_base_configuration()

    oidc_providers = authnyc['oidc_providers'].unwrap()

    return oidc_providers


@st.cache_resource
def get_oidc_api_providers():
    authnyc = get_base_configuration()

    oidc_api_providers = authnyc['oidc_api_providers'].unwrap()

    return oidc_api_providers


def ensure_clean_start():
    # Doesn't work under Windblows
    config_db_file = r'config_db.json'
    config_db_path = os.path.join(os.getcwd(), config_db_file)
    user_db_file = r'user_db.json'
    user_db_path = os.path.join(os.getcwd(), user_db_file)
    oidc_db_file = r'oidc_db.json'
    oidc_db_path = os.path.join(os.getcwd(), oidc_db_file)

    db_paths = [config_db_path, user_db_path, oidc_db_path]

    if 'oidc_discovery_form_submitted' not in st.session_state or \
        'oidc_api_form_submitted' not in st.session_state:
        for apath in db_paths:
            if os.path.exists(apath):
                os.remove(apath)
    

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
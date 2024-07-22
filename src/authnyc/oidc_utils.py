# oidc_utils.py 
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
# Date: 2024-07-19

import os
import requests
import streamlit as st
import validators

from common_utils import update_configuration
from loguru import logger
from tinydb import TinyDB, Query

def initialize_oidc_store():
    oidc_store_filename = r'oidc_store.json'
    oidc_store_path = os.path.join(os.getcwd(), oidc_store_filename)

    db = TinyDB(oidc_store_path)

    if 'oidc_store' not in st.session_state:
        st.session_state.oidc_store = db


def validate_oidc_discovery_form():
    if 'Select' in st.session_state['selected_oidc_provider']:
        if st.session_state['oidc_discovery_url'] is None or \
            st.session_state['oidc_client_id'] is None or \
            st.session_state['oidc_client_secret'] is None or \
            st.session_state['redirect_uri'] is None:
            return False
        return False
    else:
        disc_url = st.session_state['oidc_discovery_url']
        disc_url_valid = validators.url(disc_url)

        if disc_url_valid:
            oidc_provider = parse_oidc_configuration()
            save_oidc_provider(oidc_provider)
            return True
        
        return False


def validate_oidc_api_form():
    if 'Select' in st.session_state['selected_oidc_api_provider']:
        if st.session_state['api_domain'] is None or \
            st.session_state['api_client_id'] is None or \
            st.session_state['api_client_secret'] is None or \
            st.session_state['api_audience'] is None:
            return False
        return False
    else:
        save_oidc_api_provider()
        return True


def parse_oidc_configuration():
    oidc_provider = {}
    oidc_config = {}
    client_config = {}
    response = requests.get(st.session_state['oidc_discovery_url'])
    logger.debug("OIDC configuration response...{}", response.json())
    oidc_config['provider'] = response.json()
    client_config['client_id'] = st.session_state['oidc_client_id']
    client_config['client_secret'] = st.session_state['oidc_client_secret']
    client_config['redirect_uri'] = st.session_state['redirect_uri']
    oidc_config['client'] = client_config
    oidc_provider[st.session_state['selected_oidc_provider']] = oidc_config

    logger.debug("OIDC provider configuration...{}", oidc_provider)

    return oidc_provider


def save_oidc_provider(oidc_provider):
    logger.debug("OIDC provider to be saved...{}", oidc_provider)
    if 'oidc_store' not in st.session_state:
        initialize_oidc_store()

    oidc_store = st.session_state['oidc_store']
    oidc_store.insert(oidc_provider)

    st.session_state['oidc_provider_configured'] = True


def save_oidc_api_provider():
    api_provider = {}
    api_config = {}
    selected_oidc_api_provider = st.session_state['selected_oidc_api_provider']
    api_name = selected_oidc_api_provider

    api_config['api_domain'] = st.session_state['api_domain']
    api_config['api_client_id'] = st.session_state['api_client_id']
    api_config['api_client_secret'] = st.session_state['api_client_secret']
    api_config['api_audience'] = st.session_state['api_audience']

    api_provider[api_name] = api_config
    logger.debug("OIDC API provider to be saved...{}", api_provider)
    
    if 'oidc_store' not in st.session_state:
        initialize_oidc_store()

    oidc_store = st.session_state['oidc_store']
    oidc_store.insert(api_provider)

    update_configuration()


def get_oidc_provider_config():
    if 'app_config' in st.session_state:
        app_config = st.session_state['app_config']

        oidc_provider_name = app_config['oidc_provider_name']

        return lookup_provider(oidc_provider_name)

def lookup_provider(name):
    if 'oidc_store' not in st.session_state:
        initialize_oidc_store()

    oidc_store = st.session_state['oidc_store']
    Provider = Query()
    provider_record = oidc_store.search(Provider.name == name)
    if not provider_record:
        logger.info("OIDC provider not found, search result...{}", provider_record)
        provider_record = None
    else:
        logger.debug("OIDC provider found...{}", provider_record[0])
        provider_record = dict(provider_record[0])

    return provider_record

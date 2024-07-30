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

import date_utils as du
import os
import requests
import streamlit as st
import uuid
import validators

from common_utils import update_base_configuration, save_configuration
from common_utils import get_oidc_providers, get_oidc_api_providers
from loguru import logger
from tinydb import TinyDB, Query


@st.cache_resource
def get_oidc_db():
    oidc_db_file = r'oidc_db.json'
    oidc_db_path = os.path.join(os.getcwd(), oidc_db_file)

    db = TinyDB(oidc_db_path)

    return db
    

def get_provider_config(provider_key):
    #logger.debug("Get OIDC provider config - state...{}", st.session_state)
    return lookup_provider(provider_key)


def get_oidc_provider_names():
    oidc_providers = get_oidc_providers()
    return oidc_providers.keys()


def get_oidc_api_provider_names():
    oidc_api_providers = get_oidc_api_providers()
    return oidc_api_providers.keys()


def validate_oidc_discovery_form():
    if 'Select' in st.session_state['selected_oidc_provider']:
        if not st.session_state['oidc_discovery_url'] or \
            st.session_state['oidc_client_id'] or \
            st.session_state['oidc_client_secret'] or \
            st.session_state['oidc_redirect_uri']:
            return False
        return False
    else:
        disc_url = st.session_state['oidc_discovery_url']
        disc_url_valid = validators.url(disc_url)

        if 'redirect_uri' not in st.session_state:
            st.session_state['redirect_uri'] = \
                st.session_state['oidc_redirect_uri']
            
        if 'client_id' not in st.session_state:
            st.session_state['client_id'] = st.session_state['oidc_client_id']

        if disc_url_valid:
            oidc_provider = parse_oidc_configuration()
            save_oidc_provider(oidc_provider)
            return True

        return False


def validate_oidc_api_form():
    if 'Select' in st.session_state['selected_oidc_api_provider']:
        if not st.session_state['api_domain'] or \
            st.session_state['api_client_id'] or \
            st.session_state['api_client_secret'] or \
            st.session_state['api_audience']:
            return False
        return False
    else:
        save_oidc_api_provider()
        update_base_configuration()
        save_configuration()
        return True


def parse_oidc_configuration():
    oidc_config = {}
    client_config = {}
    response = requests.get(st.session_state['oidc_discovery_url'])
    
    oidc_config['provider'] = response.json()
    client_config['client_id'] = st.session_state['oidc_client_id']
    client_config['client_secret'] = st.session_state['oidc_client_secret']
    client_config['redirect_uri'] = st.session_state['oidc_redirect_uri']
    oidc_config['client'] = client_config
    #logger.debug("OIDC provider configuration...{}", oidc_config)

    return oidc_config


def save_oidc_provider(oidc_config):
    oidc_provider = {}
    provider_name = st.session_state['selected_oidc_provider']
    oidc_providers = get_oidc_providers()
    provider_key = get_provider_key(oidc_providers, provider_name)

    existing_record = lookup_provider(provider_key)
    if existing_record is None:
        id = str(uuid.uuid4())
        date_format = '%Y-%m-%d %H:%M:%S'
        inserted_at = du.convert_date(format=date_format)

        oidc_provider['id'] = id
        oidc_provider['inserted_at'] = inserted_at
        oidc_provider['updated_at'] = inserted_at
        oidc_provider['name'] = provider_key
        oidc_provider['config'] = oidc_config
        oidc_db = get_oidc_db()
        oidc_db.insert(oidc_provider)

    if 'oidc_provider_key' not in st.session_state:
        st.session_state['oidc_provider_key'] = provider_key

    if 'logout_endpoint' not in st.session_state:
        st.session_state['logout_endpoint'] = \
            oidc_config['provider']['end_session_endpoint']

    #logger.debug("Saved OIDC provider - state...{}", st.session_state)


def save_oidc_api_provider():
    logger.debug("Save OIDC API provider - state...{}", st.session_state)
    api_provider = {}
    provider = {}
    api_config = {}
    provider_name = st.session_state['selected_oidc_api_provider']
    oidc_api_providers = get_oidc_api_providers()
    provider_key = get_provider_key(oidc_api_providers, provider_name)
    existing_record = lookup_provider(provider_key)
    if existing_record is None:
        api_config['api_domain'] = st.session_state['api_domain']
        api_config['api_client_id'] = st.session_state['api_client_id']
        api_config['api_client_secret'] = st.session_state['api_client_secret']
        api_config['api_audience'] = st.session_state['api_audience']

        id = str(uuid.uuid4())
        date_format = '%Y-%m-%d %H:%M:%S'
        inserted_at = du.convert_date(format=date_format)

        api_provider['id'] = id
        api_provider['inserted_at'] = inserted_at
        api_provider['updated_at'] = inserted_at
        api_provider['name'] = provider_key
        provider['provider'] = api_config
        api_provider['config'] = provider
        
        oidc_db = get_oidc_db()
        oidc_db.insert(api_provider)

    if 'oidc_api_provider_key' not in st.session_state:
        st.session_state['oidc_api_provider_key'] = provider_key

    st.session_state['oidc_provider_configured'] = True

    #logger.debug("Saved OIDC API provider - state...{}", st.session_state)


def lookup_provider(name):
    oidc_db = get_oidc_db()
    Provider = Query()
    provider_record = oidc_db.search(Provider.name == name)
    if not provider_record:
        #logger.debug("Provider not found, search result...{}", provider_record)
        provider_record = None
    else:
        #logger.debug("Provider found...{}", provider_record[0])
        provider_record = dict(provider_record[0])

    return provider_record


def get_provider_key(providers, name):
    for k, v in providers.items():
        if k == name:
            return v
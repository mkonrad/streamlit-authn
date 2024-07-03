# zodb_utils.py 
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
# Date: 2024-07-02

import authnyc_user
import BTrees.OOBTree
import common_utils as cu
import os
import streamlit as st
import transaction
import ZODB, ZODB.FileStorage

from streamlit.logger import get_logger

logger = get_logger(__name__)


def initialize_zodb_storage():
    user_store_filename = r'user_store.fs'
    user_store_path = os.path.join(cu.app_dir(), user_store_filename)
    storage = ZODB.FileStorage.FileStorage(user_store_path)

    return storage


def initialize_zodb():
    storage = initialize_zodb_storage()
    db = ZODB.DB(storage)

    return db

def open_user_store():
    db = initialize_zodb()
    connection = db.open()
    root = connection.root()

    root.users = BTrees.OOBTree.BTree()

    if 'user_store' not in st.session_state:
        st.session_state.user_store = root.users


def finduser(email):
    if 'user_store' not in st.session_state:
        open_user_store()

    user_store = st.session_state.user_store

    try:
        user = user_store[email]
    except KeyError as e:
        logger.info(e)
        return None

    return user


def adduser(user):
    if 'user_store' not in st.session_state:
        open_user_store()

    user_store = st.session_state.user_store

    if user is not None:
        user_store[user.email] = user
        transaction.commit()
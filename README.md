# AUTHn! - A Streamlit Authentication Demonstration Application


## Prerequisites


Python 3.12.4
Editor of choice


## Running AUTHn!


After downloading the repository, the .env file needs to be created if 
testing OAuth 2 authentication. See the `Historical Documentation` section 
for details on how to create the .env file. 

If testing username/password authentication see the `Historical Documentation` 
on how to change app.py.

Create a python virtual environment in the same directory as the repository 
download. See `Historical Documentation`.

With the virtual environment active run the following command to install 
the python dependencies:

    pip install -r requirements.txt


After making these changes; run the following command to start AUTHn!:

    streamlit run ./src/app/app.py
    

# Historical Documentation
---

## Setup Python Virtual Environment


Windows:

    py -m venv .\venv


macOS: 

    python3 -m venv ./venv


### Activate the Python Virtual Environment


Windows: 

    .\venv\Scripts\Activate.ps1

>  
> (venv) C:\path\to\project>
>  


macOS:

    . ./venv/bin/activate


## Install Python Dependencies


    pip install flask
    pip install streamlit
    pip install streamlit-authenticator
    pip install streamlit-oauth
    

## Create Application Directory Structure


    mkdir -p src/app/images

    mkdir src/app/docs

    mkdir src/app/.streamlit
    

## Create Application Entrypoint


Edit src\app\app.py

app.py content
`
# app.py 
# Description: A basic streamlit application
# Author(s): Michael Konrad (c) 2024 All rights reserved.
# Date: 2024-06-19

import streamlit as st

from streamlit.logger import get_logger

logger = get_logger(__name__)

st.set_page_config(
    page_title="My Account",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://community.auth0.com'
    }
)

def main():
    st.header('Welcome to AUTHn!')


if __name__ == "__main__":
    main()
`

AUTHn! is now runnable. Run the following command to start the 
the server:


Ensure the virtual environment is activated prior to launching Streamlit.


  (venv)  streamlit run ./src/app/app.py


>  
>  You can now view your Streamlit app in your browser.  
>  
>  Local URL: http://localhost:8501  
>  


## Add a Common Utilities module


Edit src/app/common_utils.py


`
# common_utils.py 
# Description: A basic streamlit application
# Author(s): Michael Konrad (c) 2024 All rights reserved.
# Date: 2024-06-19

import os

# Utility method to determine where the application is running from.
def app_dir():
    start_path = os.path.realpath(__file__)
    wd = os.path.dirname(start_path)

    return wd

# Utility method for retrieving a logo from the images directory.
def get_logo(logo='logo.png'):
    return os.path.join(app_dir(), r'images', logo')
`

## Logos

Copy application specific logos to the src/app/images directory.


## Update app.py


Add the logos to the Streamlit app:

`
# app.py 
# Description: A basic streamlit application
# Author(s): Michael Konrad (c) 2024 All rights reserved.
# Date: 2024-06-19

import streamlit as st
import common_utils as cu

from streamlit.logger import get_logger

logger = get_logger(__name__)

logo = cu.get_png_logo()

st.set_page_config(
    page_title="AUTHn",
    page_icon=logo,
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://community.auth0.com'
    }
)

def main():
    st.logo(logo)
    st.header('Welcome to AUTHn!')


if __name__ == "__main__":
    main()
`


## Set Some Streamlit Defaults


Edit `src/app/.streamlit/config.toml`


`
[theme]
base="light"
primaryColor=#0079c2
secondaryBackgroundColor=#92d3f5
`


## Add Basic Username/Password Authentication


Based on: 
https://github.com/mkhorasani/Streamlit-Authenticator/blob/main/README.md


### Built-in Test Users


Following the example, create a yaml backed user store with some 
test user accounts.

Ensure the python virtual environment is activate prior to beginning this 
step.


#### Create Hashed Passwords

    python

    import streamlit_authenticator as stauth

    hashed_passwords = stauth.utilities.hasher.Hasher(['password1', 'password2']).generate()

    print(hashed_passwords)


Copy the hashed passwords to the creds_authenticator.yaml file to their respective accounts.


#### Generate Cookie Key

    openssl rand -hex 32

Copy the result into the creds_authenticator.yaml file under cookie > key.


Edit `src/app/creds_authenticator.yaml`


`
cookie:
  expiry_days: 30
  key: <copied-from-above-step>
  name: streamlit_app_authn
credentials:
  usernames:
    testuser1489:
      email: testuser1@test.com
      name: Test User 1
      failed_login_attempts: 0
      logged_in: false
      password: <copied-from-above-step>
    testuser1490:
      email: testuser2@test.com
      name: Test User 2
      failed_login_attempts: 0
      logged_in: false
      password: <copied-from-above-step>
preauthorized:
  emails:
  - <userid@domain.com>
  `

### Create Authentication Utility


Edit `src/app/auth_utils.py`


`
# auth_utils.py 
# Description: A basic streamlit application
# Author(s): Michael Konrad (c) 2024 All rights reserved.
# Date: 2024-06-19

import common_utils as cu
import os
import streamlit_authenticator as stauth
import yaml

from urllib.parse import quote_plus, urlencode
from yaml.loader import SafeLoader

def initialize_creds_authenticator():
    wd = cu.app_dir()
    config_file = r'creds_authenticator.yaml'
    auth_config_path = os.path.join(wd, config_file)

    with open(auth_config_path) as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['pre-authorized']
    )

    return authenticator


def confirm_creds_session(authenticator):
    name, authentication_status, username = authenticator.login()

    if st.session_state["authentication_status"]:
        authenticator.logout(location='sidebar')
        st.write(f'Welcome *{st.session_state["name"]}*')
        st.title('Bringing some :sun_with_face:')
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
`

### Update app.py with Basic Authentication


Update app.py to initialize the authenticator and add session management:

`
# app.py 
# Description: A basic streamlit application
# Author(s): Michael Konrad (c) 2024 All rights reserved.
# Date: 2024-06-19

import auth_utils as au
import common_utils as cu
import streamlit as st

from streamlit.logger import get_logger

logger = get_logger(__name__)
logo = cu.get_png_logo()

st.set_page_config(
    page_title="My Account",
    page_icon=logo,
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://community.auth0.com'
    }
)

def main():
    st.logo(logo)
    st.header('Welcome to AUTHn!')

    authenticator = au.initialize_creds_authenticator()
    au.confirm_creds_session(authenticator)


if __name__ == "__main__":
    main()
`

## Add OAuth 2 Authentication


Based on:
https://github.com/dnplus/streamlit-oauth


This configuration requires an OAuth 2 service provider. This setup will 
cover the use of Auth0. Visit https://auth0.com to create an account. 


### Create Auth0 Application Definition

1. Login to the Auth0 Dashboard
2. Select Applications > Applications
3. Select `+ Create Application`
  a. Name: streamlit-app
  b. Choose an application type: Regular Web Applications
  c. Select Create
4. Select Python for `What technology are you using for your project?`

1. Select Settings
2. Update Allowed Callback URLs
  a. http://localhost:8501
3. Update Allowed Logout URLs
  a. http://localhost:8501
4. Select Save Changes


The following information will be used to create the .env file for 
instantiating OAuth 2. 

From `Settings` copy these fields to the environment file:
- CLIENT_ID
- CLIENT_SECRET

On the `Settings` page scroll to the bottom and select Advanced Settings > 
Endpoints

Use these properties to populate these fields in the environment file:
- AUTHORIZE_URL
- TOKEN_URL
- REFRESH_TOKEN_URL
- REVOKE_TOKEN_URL


### Create Environment File 


Create the environment file to store OAuth 2 settings:


Edit `src/app/.env`

`
AUTHORIZE_URL=https://<auth0_domain_url>/authorize
TOKEN_URL=https://<auth0_domain_url>/oauth/token
REFRESH_TOKEN_URL=https://<auth0_domain_url>/oauth/token
REVOKE_TOKEN_URL=https://<auth0_domain_url>/oauth/revoke
CLIENT_ID=<AUTH0_CLIENT_ID>
CLIENT_SECRET=<AUTH0_CLIENT_SECRET>
`

### Update Authenticator Utility


1. Update imports:


`
import common_utils as cu
import base64
import json
import os
import streamlit as st
import streamlit_authenticator as stauth
import yaml

from dotenv import load_dotenv
from flask import redirect
from streamlit.logger import get_logger
from streamlit_oauth import OAuth2Component
from urllib.parse import quote_plus, urlencode
from yaml.loader import SafeLoader
`

2. Add OAuth 2 initializer:


`
def initialize_token_authenticator():
    # Load environment variables from .env file
    load_dotenv()

    # Set environment variables
    AUTHORIZE_URL = os.environ.get('AUTHORIZE_URL')
    TOKEN_URL = os.environ.get('TOKEN_URL')
    REFRESH_TOKEN_URL = os.environ.get('REFRESH_TOKEN_URL')
    REVOKE_TOKEN_URL = os.environ.get('REVOKE_TOKEN_URL')
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

    return OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_URL, 
                           TOKEN_URL, REFRESH_TOKEN_URL, REVOKE_TOKEN_URL)
`

3. Add logout state and action:


`
def logout_button():
    st.session_state.logout = True
    logout()
        

def logout():
    LOGOUT_URL = os.environ.get('LOGOUT_URL')
    CLIENT_ID = os.environ.get('CLIENT_ID')
    if st.session_state.logout:
        del st.session_state.first_name
        del st.session_state.last_name
        del st.session_state.auth_email
        del st.session_state.token

        logger.info("Calling redirect...")
        return redirect(LOGOUT_URL + "?" + urlencode(
            {
                "returnTo": 'http://localhost:8051',
                "client_id": CLIENT_ID,
            },
            quote_via=quote_plus,
            )
        )
`


4. Add OAuth 2 session confirmation:


Auth0 favicon.ico: 
    https://cdn.auth0.com/quantum-assets/dist/latest/favicons/auth0-favicon-onlight.png


`
def confirm_token_session(authenticator):
    if 'auth_email' not in st.session_state:
        result = authenticator.authorize_button(
            name='Log in with Auth0',
            icon='https://cdn.auth0.com/quantum-assets/dist/latest/favicons/auth0-favicon-onlight.png',
            redirect_uri='http://localhost:8501',
            scope="openid email profile",
            key='auth0_btn'
            extras_params={"prompt": "consent", "access_type": "offline"},
            use_container_width=False,
            pkce='S256',
        )

        if result:
            st.write(result)
            # decode the id_token jwt and get the user's email address
            id_token = result["token"]["id_token"]
            # verify the signature is an optional step for security
            payload = id_token.split(".")[1]
            # add padding to the payload if needed
            payload += "=" * (-len(payload) % 4)
            payload = json.loads(base64.b64decode(payload))
            auth_email = payload['email']
            first_name = payload['given_name']
            last_name = payload['family_name']
            if 'auth' not in st.session_state:
                st.session_state['auth_email'] = auth_email
            if 'first_name' not in st.session_state:
                st.session_state['first_name'] = first_name
            if 'last_name' not in st.session_state:
                st.session_state['last_name'] = last_name
            if 'token' not in st.session_state:
                st.session_state['token'] = result['token']

    else:
        st.write(f'Welcome *{st.session_state["first_name"]}* *{st.session_state["last_name"]}*')
        st.write('Bringing some :sun_with_face:')
        st.write(st.session_state['auth_email'])
        st.write(st.session_state['token'])
        st.button("Logout", on_click=logout_button)
`


### Modify app.py for OAuth 2 Initializer and Session


Change the creds_authenticator to the token_authenticator and update 
creds_session to token_session.

`
...
def main():
    st.logo(logo)
    st.header('Welcome to AUTHn!')
    
    __authenticator = au.initialize_token_authenticator()__
    au.confirm_token_session(authenticator)


if __name__ == "__main__":
    main()
`
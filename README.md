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
    

## Application Entrypoint


    src/app/app.py


## Add a Common Utilities module


General application wide utility module.


    src/app/common_utils.py


## Logos


Copy application specific logos to the src/app/images directory.



## Set Some Streamlit Defaults


Edit 

    src/app/.streamlit/config.toml


`
[theme]
base="light"
primaryColor=#0079c2
secondaryBackgroundColor=#92d3f5
`


## Basic Username/Password Authentication


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


Edit 

    src/app/creds_authenticator.yaml


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


## Authentication Utility


A utility module for managing authentication.


    src/app/auth_utils.py


## Update app.py with Basic Authentication


Authentication and session management is done with 2 calls to the auth_utils 
module: 


def main():
    st.logo(logo)
    st.header('Welcome to AUTHn!')

    __authenticator = au.initialize_creds_authenticator()__
    __au.confirm_creds_session(authenticator)__



## Add OAuth 2 Authentication


Based on:
https://github.com/dnplus/streamlit-oauth


This configuration requires an OAuth 2 service provider. This setup will 
cover the use of Auth0. Visit `https://auth0.com` to create an account. 


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


Edit 

    src/app/.env

`
AUTHORIZE_URL=https://<auth0_domain_url>/authorize
TOKEN_URL=https://<auth0_domain_url>/oauth/token
REFRESH_TOKEN_URL=https://<auth0_domain_url>/oauth/token
REVOKE_TOKEN_URL=https://<auth0_domain_url>/oauth/revoke
CLIENT_ID=<AUTH0_CLIENT_ID>
CLIENT_SECRET=<AUTH0_CLIENT_SECRET>
`



### Switching app.py for OAuth 2 Initializer and Session


Change the creds_authenticator to the token_authenticator and update 
creds_session to token_session.


def main():
    st.logo(logo)
    st.header('Welcome to AUTHn!')
    
    __authenticator = au.initialize_token_authenticator()__
    __au.confirm_token_session(authenticator)__

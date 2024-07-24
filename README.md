# Authnyc! - A Streamlit Authentication Demonstration Application


## OS Prerequisites


Python 3.12.4


## Application Prerequisites


### OAuth 2 Authentication


Based on:
https://github.com/dnplus/streamlit-oauth


This configuration requires an OAuth 2 service provider. This setup will 
cover the use of Auth0. Visit `https://auth0.com` to create an account. 


### Create Auth0 Application


1. Login to the Auth0 Dashboard
2. Select Applications > Applications
3. Select `+ Create Application`
  a. Name: streamlit-app
  b. Choose an application type: Regular Web Applications
  c. Select Create
4. Select Python for `What technology are you using for your project?`

5. Select Settings
6. Update Allowed Callback URLs
  a. http://localhost:8501
7. Update Allowed Logout URLs
  a. http://localhost:8501
8. Select Save Changes


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
LOGOUT_URL=https://<auth0_domain_url>/v2/logout
REDIRECT_URI=http(s)://<app_fqdn:port>
EDIT_PROFILE=True
`


## Running Authnyc!


First time run; create a python virtual environment in the root directory of 
Authnyc!.

See the `Historical Documentation` section for details on the virtual 
environment.


### Install Dependencies (One Time Setup)

1. Activate Virtual Environment

Windows:

    .\venv\Scripts\Activate.ps1


macOS:

    . ./venv/bin/activate


2. Install Dependencies

    pip install -r requirements.txt


3. Run the following command to start Authnyc!:

    streamlit run ./src/authnyc/authnyc.py


## Authnyc User Profile


User profile support has been added to Authnyc!. 

To support editing `My Profile`, a Machine to Machine application needs to be 
configured in Auth0 and a .apienv file is added to Authnyc in the 
`src/authnyc` directory. 


### Create Auth0 Machine to Machine Application

 
1. Login to Auth0 Dashboard 
2. Select Applications -> Applications 
3. Select Create Application 
4. Set Application Name 
5. Select Machine to Machine Applications 
6. Select Create  
7. Select API 
8. Select the following scopes: 
  a. read:users 
  b. update:users 
  c. create:users 
  d. read:users_app_metadata 
  e. update:users_app_metadata 
  f. create:users_app_metadata 
9. Select Authorize 


### Update API (Machine to Machine) Environment File


Update the .apienv file as per your Auth0 Machine to Machine configuration:

`
API_DOMAIN=<your_auth0_api_domain>
API_CLIENT_ID=<your_auth0_api_client_id>
API_CLIENT_SECRET=<your_auth0_api_client_secret>
API_AUDIENCE=https://<your_auth0_api_domain>/api/v2/
`

After updating the .env and .apienv files uncomment these settings in the 
`.gitignore` file so your secrets are not copied to version control. 
    

# Historical Documentation
---

## Setup Python Virtual Environment


Setting up the python virtual environment is a one time step. 


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


## Pip Upgrade

    python.exe -m pip install --upgrade pip

## Logos


Copy application specific logos to the src/app/images directory.


## Set Some Streamlit Defaults


Edit 

    .streamlit/config.toml


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
    testuser1:
      email: testuser1@test.com
      name: Test User 1
      failed_login_attempts: 0
      logged_in: false
      password: <copied-from-above-step>
    testuser2:
      email: testuser2@test.com
      name: Test User 2
      failed_login_attempts: 0
      logged_in: false
      password: <copied-from-above-step>
preauthorized:
  emails:
  - <userid@domain.com>
` 


## Update authnyc.py with Basic Authentication


Authentication and session management is done with 2 calls to the auth_utils 
module: 


def main():
    st.logo(logo)
    st.header('Welcome to Authnyc!')

    __authenticator = au.initialize_creds_authenticator()__
    __au.confirm_creds_session(authenticator)__


### Switching authnyc.py for OAuth 2 Initializer and Session (Default)


Change the creds_authenticator to the token_authenticator and update 
creds_session to token_session.


def main():
    st.logo(logo)
    st.header('Welcome to Authnyc!')
    
    __authenticator = au.initialize_token_authenticator()__
    __au.confirm_token_session(authenticator)__
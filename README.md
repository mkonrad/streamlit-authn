# Authnyc! - A Streamlit Authentication Demonstration Application

Authnyc! is a OpenID Connect client demonstration application. 

Authnyc! has been tested with and currently only has pre-programmed support 
for integrating with Auth0 as a provider. 



## OS Prerequisites


Python 3.12.x


## Application Prerequisites


### Auth0 Tenant Requirements


#### Create an Application


1. Login to the Auth0 Dashboard
2. Select Applications > Applications
3. Select `+ Create Application`
  a. Name: SampleApp
  b. Choose an application type: Regular Web Applications
  c. Select Create
4. Select Python for `What technology are you using for your project?`

5. Select Settings
6. Update Allowed Callback URLs
  a. http://localhost:8501
7. Update Allowed Logout URLs
  a. http://localhost:8501
8. Select Save Changes


#### Create a Machine to Machine Application

 
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


## Running Authnyc!


1. Set up Python Virtual Environment (one time step) 


Windows:

    py -m venv .\venv


macOS: 

    python3 -m venv ./venv


2. Activate Virtual Environment

Windows:

    .\venv\Scripts\Activate.ps1


macOS:

    . ./venv/bin/activate


3. Install Dependencies (One time step)

Windows:

    python.exe -m pip install --upgrade pip

macOS:

    pip install --upgrade pip

Both:
    pip install -r requirements.txt


4. Run Authnyc!:

    streamlit run ./src/authnyc/authnyc.py


When starting Authnyc! for the first time, a couple of forms will collect 
the required provider information which will be used to automatically configure 
the OIDC client. 


To clear the configuration and start over, edit the authnyc.toml file and 
set `oidc_provider_configured = false`, remove the config_db.json, oidc_db.json, 
and user_db.json files if they exists.


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


## Set Some Streamlit Defaults


Edit 

    .streamlit/config.toml


`
[theme]
base="light"
primaryColor=#0079c2
secondaryBackgroundColor=#92d3f5
`

## OIDC Authentication


Based on:
https://github.com/dnplus/streamlit-oauth


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


https://static.vecteezy.com/system/resources/previews/000/574/829/original/vector-login-sign-icon.jpg
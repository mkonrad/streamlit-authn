# Issues


## Token Expiration ?

2024-08-22 10:10:13.588 | INFO     | auth_utils:logout:152 - Calling redirect...
2024-08-22 10:10:13.591 | INFO     | common_utils:initialize:30 - Initializing application...
2024-08-22 10:10:13.607 | DEBUG    | auth_utils:login:106 - Login state...{}
2024-08-22 11:52:28.201 | INFO     | common_utils:initialize:30 - Initializing application...
2024-08-22 11:52:28.226 | DEBUG    | auth_utils:login:106 - Login state...{}
2024-08-22 11:52:34.936 | INFO     | common_utils:initialize:30 - Initializing application...
2024-08-22 11:52:34.948 | DEBUG    | auth_utils:login:106 - Login state...{'authenticator_login': {'code': 'tDGIpqeLy6ypH-ETl3OBE3gafOQfFn84OBP2jrq63_u1A', 'state': 'd5c07d721ed94086b5b67a9e2cbfddd7'}}
2024-08-22 11:52:34.965 Uncaught app exception
Traceback (most recent call last):
  File "\venv\Lib\site-packages\streamlit\runtime\scriptrunner\script_runner.py", line 589, in _run_script
    exec(code, module.__dict__)
  File "\src\authnyc\authnyc.py", line 43, in <module>
    main()
  File "\src\authnyc\authnyc.py", line 25, in main
    make_sidebar()
  File "\src/authnyc\navigation.py", line 43, in make_sidebar
    login()
  File "\src/authnyc\auth_utils.py", line 110, in login
    result = authenticator.authorize_button(
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "\venv\Lib\site-packages\streamlit_oauth\__init__.py", line 99, in authorize_button
    raise StreamlitOauthError(f"STATE {state} DOES NOT MATCH OR OUT OF DATE")
streamlit_oauth.StreamlitOauthError: STATE dcdb41e293e84275a133b416a9bdfa40 DOES NOT MATCH OR OUT OF DATE

### Login State

{'user_record': {
        'sub': 'auth0|<identifier>', 
        'name': 'Test User 1489', 
        'nickname': 'testuser1489', 
        'given_name': 'Henry', 
        'family_name': 'James 1489', 
        'email': 'testuser1489@proton.me', 
        'phone_number': '', 
        'amr': [], 
        'id': '<identifier>', 
        'inserted_at': '2024-30-07 11:27:44', 
        'updated_at': '2024-08-15 18:42:05'
    }, 
'token': {
    'access_token': 'abcd...', 
    'id_token': 'efgh...', 
    'scope': 'openid profile email', 
    'expires_in': 86400, 
    'token_type': 'Bearer', 
    'expires_at': 1723848149
}, 
'authenticated': True, 
'authenticator_login': {
    'code': '7...', 
    'state': '3...'
    }
}
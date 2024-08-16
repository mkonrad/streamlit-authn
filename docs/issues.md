# Issues


## Token Expiration ?

/authnyc/user_utils.py", line 95, in login

raise StreamlitOauthError(f"STATE {state} DOES NOT MATCH OR OUT OF DATE")
streamlit_oauth.StreamlitOauthError: STATE blahblahblah DOES NOT MATCH OR OUT OF DATE

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
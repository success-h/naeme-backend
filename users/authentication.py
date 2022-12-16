import jwt
from rest_framework import exceptions
import os



def decode_access_token(token):
    key = os.getenv('JWT_SECRET')  
    try:
        payload = jwt.decode(token, key, algorithms='HS256')
        print("payload:", payload)
        return payload['user_id']
    except:
        raise exceptions.AuthenticationFailed('failed')
""" --------------------------------------------------------------------------#
# IMPORTS
# --------------------------------------------------------------------------"""


import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from ..config.config import (AUTH0_DOMAIN, ALGORITHMS, API_AUDIENCE,
                             ERR_HEADER_MISSING, ERR_BEARER_MISSING,
                             ERR_TOKEN_MISSING, ERR_BEARER_TOKEN,
                             ERR_PERMISIONS_MISSING, ERR_NOT_AUTHORIZED,
                             ERR_TOKEN_EXPIRED, ERR_INVALID_CLAIMS,
                             ERR_PARSE_TOKEN, ERR_KEY_FIND)


""" --------------------------------------------------------------------------#
# EXCEPTIONS
# --------------------------------------------------------------------------"""


# AuthError Exception: a standardized way to communicate auth failure modes.
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


""" --------------------------------------------------------------------------#
# AUTH HEADER
# --------------------------------------------------------------------------"""


# Gets the authorization header and validates it.
def get_token_auth_header():
    # Gets header.
    auth_header = request.headers.get("Authorization", None)
    # Checks for an Authorization header.
    if not auth_header:
        raise AuthError(ERR_HEADER_MISSING['error'],
                        ERR_HEADER_MISSING['status'])

    # Heater parts to list
    auth_header_parts = auth_header.split()

    # Checks that header starts with Bearer.
    if auth_header_parts[0].lower() != 'bearer':
        raise AuthError(ERR_BEARER_MISSING['error'],
                        ERR_BEARER_MISSING['status'])
    # Checks for inclusion of token.
    elif len(auth_header_parts) == 1:
        raise AuthError(ERR_TOKEN_MISSING['error'],
                        ERR_TOKEN_MISSING['status'])
    elif len(auth_header_parts) > 2:
        raise AuthError(ERR_BEARER_TOKEN['error'],
                        ERR_BEARER_TOKEN['status'])

    # Get token from header and return.
    return auth_header_parts[1]


# Checks that permissions are included in the payload.
def check_permissions(permission, payload):
    # Check payload for permissions.
    if 'permissions' in payload:
        # Check that required permission is in permissions.
        if permission not in payload['permissions']:
            raise AuthError(ERR_NOT_AUTHORIZED['error'],
                            ERR_NOT_AUTHORIZED['status'])
    else:
        raise AuthError(ERR_PERMISIONS_MISSING['error'],
                        ERR_PERMISIONS_MISSING['status'])

    return True


# Verifies authorization token, and returns payload
def verify_decode_jwt(token):
    # Get the public key from Auth0.com
    jsonurl = urlopen('https://'+AUTH0_DOMAIN+'/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    # Get the token from the header.
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    # Converts public keys to dict.
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    # Verify the token
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://'+AUTH0_DOMAIN+'/'
            )
        except jwt.ExpiredSignatureError:
            raise AuthError(ERR_TOKEN_EXPIRED['error'],
                            ERR_TOKEN_EXPIRED['status'])
        except jwt.JWTClaimsError:
            raise AuthError(ERR_INVALID_CLAIMS['error'],
                            ERR_INVALID_CLAIMS['status'])
        except Exception:
            raise AuthError(ERR_PARSE_TOKEN['error'],
                            ERR_PARSE_TOKEN['status'])
        _request_ctx_stack.top.current_user = payload
        return payload

    raise AuthError(ERR_KEY_FIND['error'],
                    ERR_KEY_FIND['status'])


# Decorator for methods that require authorization and
# specific permissions.
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator

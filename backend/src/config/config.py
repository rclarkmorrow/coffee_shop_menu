""" --------------------------------------------------------------------------#
# AUTHORIZATION CONFIG
# --------------------------------------------------------------------------"""


AUTH0_DOMAIN = 'rclarkmorrow.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'menu'


""" --------------------------------------------------------------------------#
# AUTHORIZATION ERRROR MESSAGES
# --------------------------------------------------------------------------"""


ERR_HEADER_MISSING = {
    'error': {'code': 'authorization_header_missing',
              'descripion': 'authorization header expected'},
    'status': 401
}
ERR_BEARER_MISSING = {
    'error': {'code': 'invalid_header',
              'description': 'Authorization header must start with bearer'},
    'status': 401
}
ERR_TOKEN_MISSING = {
    'error': {'code': 'invalid_header',
              'description': 'Token not found'},
    'status': 401
}
ERR_BEARER_TOKEN = {
    'error': {'code': 'invalid_header',
              'description': 'Authorization header must be Bearer token'},
    'status': 401
}
ERR_PERMISIONS_MISSING = {
    'error': {'code': 'not_authorized',
              'description': 'Permissions not included in payload'},
    'status': 400
}
ERR_NOT_AUTHORIZED = {
    'error': {'code': 'not_authorized',
              'description': 'Token not authorized for this request'},
    'status': 401
}
ERR_TOKEN_EXPIRED = {
    'error': {'code': 'expired_token',
              'description': 'This token has expired'},
    'status': 401
}
ERR_INVALID_CLAIMS = {
    'error': {'code': 'invalid_claims',
              'description': 'incorrect claims, please check'
              ' the audience and issuer'},
    'status': 401
}
ERR_PARSE_TOKEN = {
    'error': {'code': 'invalid_header',
              'description': 'Unable to parse authentication token'},
    'status': 400
}
ERR_KEY_FIND = {
    'error': {'code': 'invalid_header',
              'description': 'Unable to find appropriate key'},
    'status': 401
}

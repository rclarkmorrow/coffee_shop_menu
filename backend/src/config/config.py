""" --------------------------------------------------------------------------#
# AUTHORIZATION CONFIG
# --------------------------------------------------------------------------"""


AUTH0_DOMAIN = 'rclarkmorrow.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'menu'


""" --------------------------------------------------------------------------#
# AUTHORIZATION ERRROR MESSAGES
# --------------------------------------------------------------------------"""


ERR_HEADER_MISSING = ({'code': 'authorization_header_missing"'},
                      {'description': 'authorization header is expected'}, 401)
ERR_BEARER_MISSING = ({'code': 'invalid_header'},
                      {'description': 'Authorization header must start'
                       ' with bearer'}, 401)
ERR_TOKEN_MISSING = ({'code': 'invalid_header'},
                     {'description': 'Token not found'}, 401)
ERROR_BEARER_TOKEN = ({'code': 'invalid_header'},
                      {'description': 'Authorization header must be'
                      ' Bearer token'}, 401)

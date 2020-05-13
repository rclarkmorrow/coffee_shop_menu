""" --------------------------------------------------------------------------#
# IMPORTS
# --------------------------------------------------------------------------"""


import os
import json
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
from flask_cors import CORS
from types import SimpleNamespace

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth
from .controllers.controllers import Drinks


""" --------------------------------------------------------------------------#
# CREATE CORS APP AND DATABASE
# --------------------------------------------------------------------------"""


app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''

db_drop_and_create_all()


""" --------------------------------------------------------------------------#
# ROUTES
# --------------------------------------------------------------------------"""


@app.route('/drinks', methods=['GET', 'POST'])
def get_or_post_drinks():
    # Respond to GET request.
    if request.method == 'GET':
        this_menu = Drinks()
        this_menu.get_menu()
        return this_menu.response
    # Respond to POST request.
    elif request.method == 'POST':
        @requires_auth('post:drinks')
        def post_drink(jwt):
            this_request = request.get_json()
            if 'title' in this_request and 'recipe' in this_request:
                form_data = SimpleNamespace(**this_request)
                this_drink = Drinks(form_data=form_data)
                this_drink.create_drink()
                return this_drink.response
            else:
                abort(500)
        return post_drink()
    else:
        abort(500)


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    return jsonify({'success': True,
                    'message': 'not implemented'})


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<id>', methods=['PATCH', 'DELETE'])
def patch_or_delete_drinks(id):
    if request.method == 'PATCH':
        @requires_auth('patch:drinks')
        def patch_drink(jwt):
            return jsonify({'success': True,
                            'message': 'not implemented'})

        return patch_drink()
    elif request.method == 'DELETE':
        @requires_auth('delete:drinks')
        def delete_drink(jwt):
            return jsonify({'succes': True,
                           'message':  'not implemented'})

        return delete_drink()
    else:
        abort(500)


""" --------------------------------------------------------------------------#
# ERROR_HANDLING
# --------------------------------------------------------------------------"""


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        'success': False,
        'error': error.status_code,
        'message': error.error
    }), error.status_code


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'method not allowed'
    }), 405


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'unprocessable'
    }), 422


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'succes': False,
        'error': 500,
        'message': 'internal server error'
    }), 500

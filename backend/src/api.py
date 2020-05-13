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

# Route handles showing the public the drink menu and the manager
# role's ability to add new drinks to the menu.
@app.route('/drinks', methods=['GET', 'POST'])
def get_or_post_drinks():
    # Respond to GET request.
    if request.method == 'GET':
        # Get a menu as a Drinks object with the
        # method that returns a list of shortened drinks.
        this_menu = Drinks()
        this_menu.get_menu()
        # Return Drinks object JSON response property.
        return this_menu.response
    # Respond to POST request.
    elif request.method == 'POST':
        # Wrap function to verify authorization.
        @requires_auth('post:drinks')
        def post_drink(jwt):
            this_request = request.get_json()
            # Check request for required data, abort if not included.
            if 'title' in this_request and 'recipe' in this_request:
                # Structure data and pass to Drinks object.
                form_data = SimpleNamespace(**this_request)
                this_drink = Drinks(form_data=form_data)
                this_drink.create_drink()
                # Return Drinks object JSON response property.
                return this_drink.response
            else:
                abort(422)
        return post_drink()
    else:
        abort(500)


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    # Get a list of recipies as a Drinks object with the
    # metod that returns a list of lengthened drinks.
    these_recipies = Drinks()
    these_recipies.get_recipies()
    # Return Drinks ojbect JSON response property.
    return these_recipies.response


@app.route('/drinks/<id>', methods=['PATCH', 'DELETE'])
def patch_or_delete_drinks(id):
    # If id is not an integer, convert it to one if possible,
    # otherwise return the integer or original variable.
    id = int(str(id)) if str(id).isdigit() else id
    # Exit with 422 if id is not an int.
    if type(id) != int:
        abort(422)
    # Respond to PATCH request.
    if request.method == 'PATCH':
        # Wrap function to verify authorization.
        @requires_auth('patch:drinks')
        def patch_drink(jwt):
            this_response = request.get_json()
            if 'title' in this_response or 'recipe' in this_response:
                form_data = SimpleNamespace(**this_response)
                this_drink = Drinks(form_data=form_data, id=id)
                this_drink.edit_drink()
                # Check for error, abort with error code.
                if this_drink.status.error:
                    abort(this_drink.status.code)
                # Response OK, return Drinks JSON response property.
                else:
                    return this_drink.response
            else:
                abort(422)
        return patch_drink()
    # Respond to DELETE request.
    elif request.method == 'DELETE':
        # Wrap function to verify authorization.
        @requires_auth('delete:drinks')
        def delete_drink(jwt):
            this_drink = Drinks(id=id)
            this_drink.delete_drink()
            # Check for error, abort with error code.
            if this_drink.status.error:
                abort(this_drink.status.code)
            # Response OK, return Drinks JSON response property.
            else:
                return this_drink.response
        # Run the DELETE request.
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

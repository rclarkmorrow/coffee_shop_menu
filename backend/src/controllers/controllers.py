""" --------------------------------------------------------------------------#
# IMPORTS
# --------------------------------------------------------------------------"""

import json
from flask import jsonify
from types import SimpleNamespace
from ..database.models import Drink

""" --------------------------------------------------------------------------#
# CONTROLLERS
# --------------------------------------------------------------------------"""


# Controller for drinks model.
class Drinks:
    # Init self with data.
    def __init__(self, form_data=None, id=None):
        self.form_data = form_data
        self.id = id
        self.response_data = SimpleNamespace(success=True)
        self.status = SimpleNamespace(error=False)

    # Returns a list of shortened drinks for main display.
    def get_menu(self):
        drinks = self.get_all_drinks()
        self.response_data.drinks = [drink.short() for drink in drinks]
        self.response = jsonify(self.response_data.__dict__), 200

    # Returns a list of long drink recipies for baristas.
    def get_recipies(self):
        drinks = self.get_all_drinks()
        self.response_data.drinks = [drink.long() for drink in drinks]
        self.response = jsonify(self.response_data.__dict__), 200

    # Adds a drink to the menu.
    def create_drink(self):
        # Builds Drink object and inserts into database.
        this_drink = Drink(
            title=self.form_data.title,
            recipe=json.dumps(self.form_data.recipe)
        )
        this_drink.insert()
        
        # Builds response data and jsonifies.
        self.response_data.drinks = [this_drink.long()]
        self.response = jsonify(self.response_data.__dict__), 200

    # Edits a drink on the menu.
    def edit_drink(self):
        # Get drink by ID
        this_drink = self.get_one_drink(self.id)
        # Check form data for changes and change drink.
        if not self.status.error:
            if hasattr(self.form_data, 'title'):
                this_drink.title = self.form_data.title
            if hasattr(self.form_data, 'recipe'):
                this_drink.recipe = self.form_data.recipe
            # Update drink and create JSON response property.
            this_drink.update()
            self.response_data.drinks = [this_drink.long()]
            self.response = jsonify(self.response_data.__dict__), 200

    # Deletes a drink from the menu.
    def delete_drink(self):
        # Get drink by ID
        this_drink = self.get_one_drink(self.id)
        # Delete drink and create JSON response property.
        if not self.status.error:
            this_drink.delete()
            self.response_data.id = self.id
            self.response = jsonify(self.response_data.__dict__), 200

    # Returns all drinks in the database.
    def get_all_drinks(self):
        return Drink.query.order_by(Drink.id).all()

    # Returns a drink by ID from the database.
    def get_one_drink(self, id):
        this_drink = Drink.query.filter(Drink.id == id).first()
        # Check that there's actually a drink, error if not.
        if this_drink is None:
            self.status.error = True
            self.status.code = 404

        return this_drink

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


class Drinks:
    def __init__(self, form_data=None):
        self.form_data = form_data
        self.response_data = SimpleNamespace(success=True)

    def get_menu(self):
        drinks = self.get_all_drinks()
        self.response_data.drinks = [drink.short() for drink in drinks]
        self.response = jsonify(self.response_data.__dict__), 200

    def get_all_drinks(self):
        return Drink.query.order_by(Drink.id).all()

    def create_drink(self):
        this_drink = Drink(
            title=self.form_data.title,
            recipe=json.dumps(self.form_data.recipe)
        )
        this_drink.insert()
        print(this_drink, ' inserted')
        self.response_data.drinks = [this_drink.long()]
        self.response = jsonify(self.response_data.__dict__), 200

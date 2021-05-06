#!/usr/bin/python3
"""
    API index view
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json


@app_views.route('/status')
def status():
    """Returns ok status"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def numberObj():
    """ Returns the number of each object by type """
    dict = {"amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)}
    return jsonify(dict)

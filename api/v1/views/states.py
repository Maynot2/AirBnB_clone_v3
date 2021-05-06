#!/usr/bin/python3
"""
    API index view
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/states', strict_slashes=False, methods = ['GET'])
def status():
    """Returns ok status"""
    return jsonify({'status': 'OK'})

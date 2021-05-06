#!/usr/bin/python3
"""
    API index view
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """Returns ok status"""
    return jsonify({'status': 'OK'})

#!/usr/bin/python3
"""
    Restfull API instenciation
"""

from api.v1.views import app_views
from flask import Flask, jsonify
import os
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """Closes storage after each url request"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """ Returns a JSON-formatted 404 status code response"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host_number = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port_number = os.getenv('HBNB_API_PORT', 5000)
    app.run(host=host_number, port=port_number, threaded=True)

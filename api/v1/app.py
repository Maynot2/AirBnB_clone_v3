#!/usr/bin/python3
"""
    Restfull API instenciation
"""

from api.v1.views import app_views
from flask import Flask
import os
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(self):
    """Closes storage after each url request"""
    storage.close()

if __name__ == "__main__":
    host_number = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port_number = os.getenv('HBNB_API_PORT', 5000)
    app.run(host=host_number, port=port_number, threaded=True)

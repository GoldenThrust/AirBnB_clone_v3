#!/usr/bin/python3
""" Airbnb API """

from api.v1.views import app_views
from models import storage
from flask import Flask, make_response, jsonify
import os
app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """ handle app teardown """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    ''' 404 page '''
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST')
    if host is None:
        host = '0.0.0.0'

    port = os.environ.get('HBNB_API_PORT')
    if port is None:
        port = '5000'

    app.run(host=host, port=port, threaded=True)

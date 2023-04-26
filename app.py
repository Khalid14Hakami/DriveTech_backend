"""A Python Flask REST API BoilerPlate (CRUD) Style"""

import argparse
import os
from flask import Flask, jsonify, make_response, g
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from routes import request_api
from flask_mysqldb import MySQL
from passlib.apps import custom_app_context as pwd_context




APP = Flask(__name__)



### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Seans-Python-Flask-REST-Boilerplate"
    }
)
APP.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###


APP.register_blueprint(request_api.get_blueprint())




@APP.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify({'error': 'Misunderstood'}), 400)


@APP.errorhandler(401)
def handle_401_error(_error):
    """Return a http 401 error to client"""
    return make_response(jsonify({'error': 'Unauthorised'}), 401)


@APP.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@APP.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({'error': 'Server error'}), 500)

    
def connect_db():
    """Connects to the specific database."""
    #Creating a connection cursor
    print("""XXXXXXXX Xxxxxxxxmxmxmxmxx""")
    cursor = mysql.connection
    return cursor

# import functools
# def json_response(action_func):
#     @functools.wraps(action_func)
#     # def create_json_response(*args, **kwargs):
#     def get_db(*args, **kwargs):
#         """Opens a new database connection if there is none yet for the
#         current application context.
#         """
#         if not hasattr(g, 'mysql_db'):
#             g.mysql_db = connect_db()
#         return g.sqlite_db

@APP.before_request
def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'mysql_db'):
        g.mysql_db = connect_db()


@APP.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'mysql_db'):
        # g.mysql_db.close()
        pass


if __name__ == '__main__':

    PARSER = argparse.ArgumentParser(
        description="Seans-Python-Flask-REST-Boilerplate")

    PARSER.add_argument('--debug', action='store_true',
                        help="Use flask debug/dev mode with file change reloading")
    ARGS = PARSER.parse_args()

    PORT = int(os.environ.get('PORT', 5000))

    ## database config
    APP.config['MYSQL_HOST'] = 'k14h.mysql.pythonanywhere-services.com'
    APP.config['MYSQL_USER'] = 'k14h'
    APP.config['MYSQL_PASSWORD'] = 'DataBaseStrongPassword'
    APP.config['MYSQL_DB'] = 'k14h$DriveTech'
    APP.config['SECRET_KEY'] = 'SECRET_KEY'
 
    mysql = MySQL(APP)

    if ARGS.debug:
        print("Running in debug mode")
        CORS = CORS(APP)
        # APP.run(host='0.0.0.0', port=PORT, debug=True)
    else:
        # APP.run(host='0.0.0.0', port=PORT, debug=False)
        pass

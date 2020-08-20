"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

users = [
    {
        "name": "Georgi",
        "todos": [
            {
                "label": "My first task", "done": "false"
            },
            {
                "label": "My second task", "done": "false"
            }
        ]
    }
]

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/todos/user/<username>', methods=['GET'])
def get_todos(username):
    for user in users:
        if user["name"] == username:
            user_todos = user["todos"]
    return jsonify(user_todos), 200

@app.route('/todos/user/<username>', methods=['POST'])
def post_todos(username):
    request_body = request.data
    print('Incoming request with the following body: ', request.data)
    decoded_data = json.loads(request_body)

    for i in range(0, len(users)):
        if users[i]["name"] == username:
            users[i]["todos"].append(decoded_data)
    return jsonify(users[i]["todos"]), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

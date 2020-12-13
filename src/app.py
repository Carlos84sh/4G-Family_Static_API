"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import json
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

jackson_family.add_member({
    "first name": "Jhon",
    "age": 33,
    "lucky number": [7, 13, 22]})
jackson_family.add_member({
     "first name": "Jane",
    "age": 35,
    "lucky number": [10, 14, 3]})
jackson_family.add_member({
     "first name": "Jimmy",
    "age": 5,
    "lucky number": [1],
    })


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


####### ALL MEMBERS Methods GET
@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
   
    return jsonify(members), 200



####### ONE MEMBER Methods GET+ID
@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):

    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    return 'Not Found', 404



###### POST MEMBER, Methods Post
@app.route('/member', methods=['POST'])
def new_member():
    member = request.get_json()
    jackson_family.add_member(member)

    return  "Member add"+jsonify(member), 200


@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = jackson_family.delete_member(id)
    print(member)
    if member:
       return "Member delete"+jsonify(member), 200
    return "Member not found, try again"

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

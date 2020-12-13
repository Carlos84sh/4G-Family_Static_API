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
"first_name":"John",
"lucky_numbers":[7, 13, 22],
"age": 33
})

jackson_family.add_member({
"first_name":"Jane",
"lucky_numbers":[10, 14, 3],
"age": 35
})

jackson_family.add_member({
"first_name":"Jimmy",
"lucky_numbers":[1],
"age": 5
})


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
 
    return jsonify(members), 200


@app.route('/member/<int:index>', methods=['GET'])
def get_person(index):

    # this is how you can use the Family datastructure by calling its methods
    person = jackson_family.get_member(index)
    if person:
        return jsonify(person), 200
    return 'Not Found', 404
    
    

@app.route('/member', methods=['POST'])
def new_person():
    cuerpo_peticion = request.data # texto plano
    cuerpo_peticion_dict = json.loads(cuerpo_peticion) # diccionario python
    jackson_family.add_member(cuerpo_peticion_dict)

    members = jackson_family.get_all_members()
    return jsonify(members), 200



@app.route('/member/<int:index>', methods=['DELETE'])
def delete_person(index):
    member = jackson_family.delete_member(index)
    # members = jackson_family.get_all_members()
    if member:
        body = {
            "done": True
        }
        return jsonify(body), 200
    return 'Not Found', 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

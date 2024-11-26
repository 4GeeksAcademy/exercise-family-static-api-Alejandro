"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
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

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    try:
        members = jackson_family()
        return jsonify(members), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/member', methods=['POST'])
def add_member():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        member = jackson_family.add_member(data)
        return jsonify(member), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    return jsonify({"error": "Member not found"}), 404

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if member:
            jackson_family.delete_member(member_id)
            return jsonify({"done": True}), 200
        return jsonify({"error": "Member not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import Donor, Volunteer

auth_bp = Blueprint('auth', __name__)

# Register a donor
@auth_bp.route('/register/donor', methods=['POST'])
def register_donor():
    data = request.get_json()
    donor_id = Donor.create_donor(data)
    return jsonify({"message": "Donor registered", "donor_id": str(donor_id)}), 201

# Register a volunteer
@auth_bp.route('/register/volunteer', methods=['POST'])
def register_volunteer():
    data = request.get_json()
    volunteer_id = Volunteer.create_volunteer(data)
    return jsonify({"message": "Volunteer registered", "volunteer_id": str(volunteer_id)}), 201

# Login route (for both Donor and Volunteer)
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_type = data.get('user_type')
    username = data.get('username')
    password = data.get('password')
    
    if user_type == 'donor':
        user = Donor.get_donor_by_id(username)
    else:
        user = Volunteer.get_volunteer_by_id(username)
        
    if user and user['password'] == password:  # Simple password check (should be hashed in real-world)
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    return jsonify({"message": "Invalid credentials"}), 401

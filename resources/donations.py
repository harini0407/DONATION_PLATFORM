from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Donation

donation_bp = Blueprint('donations', __name__)

# Create a new donation
@donation_bp.route('/donate', methods=['POST'])
@jwt_required()
def create_donation():
    data = request.get_json()
    donor_id = get_jwt_identity()  # Get current donor
    data['donor_id'] = donor_id
    donation_id = Donation.create_donation(data)
    return jsonify({"message": "Donation created", "donation_id": str(donation_id)}), 201

# Get donations of a donor
@donation_bp.route('/my_donations', methods=['GET'])
@jwt_required()
def get_donations():
    donor_id = get_jwt_identity()
    donations = Donation.get_donations()  # You can filter by donor_id here
    return jsonify([donation for donation in donations]), 200

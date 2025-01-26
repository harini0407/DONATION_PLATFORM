from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from models import Volunteer

# Create a Blueprint for volunteers
volunteer_bp = Blueprint('volunteers', __name__)

@volunteer_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    new_volunteer = Volunteer(
        name=data['name'],
        email=data['email'],
        contact_number=data['contact_number'],
        location=data['location']
    )
    db.session.add(new_volunteer)
    db.session.commit()
    return jsonify(message="Volunteer signed up successfully"), 201

@volunteer_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    volunteer = Volunteer.query.filter_by(email=data['email']).first()
    
    if volunteer and volunteer.contact_number == data['contact_number']:
        access_token = create_access_token(identity=volunteer.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message="Invalid credentials"), 401

@volunteer_bp.route('/posts', methods=['GET'])
@jwt_required()
def get_posts():
    posts = DonorPost.query.filter_by(status="Pending").all()
    return jsonify([{
        'id': post.id,
        'donor_name': post.donor_name,
        'food_type': post.food_type,
        'quantity': post.quantity,
        'pickup_address': post.pickup_address,
        'preferred_time': post.preferred_time
    } for post in posts])

@volunteer_bp.route('/posts/accept/<int:post_id>', methods=['POST'])
@jwt_required()
def accept_post(post_id):
    volunteer_id = get_jwt_identity()
    post = DonorPost.query.get(post_id)
    
    if post:
        post.status = 'Accepted'
        post.volunteer_id = volunteer_id
        db.session.commit()
        return jsonify(message="Donation accepted successfully"), 200
    else:
        return jsonify(message="Post not found"), 404

@volunteer_bp.route('/posts/status/<int:post_id>', methods=['PATCH'])
@jwt_required()
def update_status(post_id):
    volunteer_id = get_jwt_identity()
    post = DonorPost.query.get(post_id)
    
    if post and post.volunteer_id == volunteer_id:
        data = request.get_json()
        post.status = data['status']
        db.session.commit()
        return jsonify(message="Task status updated"), 200
    else:
        return jsonify(message="Post not found or Unauthorized"), 404

@volunteer_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    volunteer_id = get_jwt_identity()
    volunteer = Volunteer.query.get(volunteer_id)
    
    if volunteer:
        return jsonify({
            'name': volunteer.name,
            'email': volunteer.email,
            'contact_number': volunteer.contact_number,
            'total_donations': volunteer.total_donations,
            'location': volunteer.location
        })
    else:
        return jsonify(message="Volunteer not found"),
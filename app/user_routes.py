from flask import Blueprint, jsonify, request, session
from . import db
from .models import User
from .schemas import UserSchema
from werkzeug.security import check_password_hash, generate_password_hash


user_schema = UserSchema()

# Create a Blueprint for the user routes
user_bp = Blueprint('users', __name__)

# Helper function to verify if the user exists and is logged in
def verify_user():
    user_id = session.get('user_id') # Fetch the logged-in user's ID
    if not user_id:
        return None, jsonify({'error': 'User not logged in'}), 401

    user = User.query.get(user_id)
    if not user:
        return None, jsonify({'error': 'User not found'}), 404

    return user, None, None  # Return user, response, and status code

# Create a new user
@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    # Ensure required fields are added
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Missing required fields-username, email or password'}), 400
    
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({'error': 'Email already in use'}), 400

    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({'error': 'Username already taken'}), 400

    if len(data.get('password')) < 8:
        return jsonify({'error': 'Password should be at least 8 characters long'}), 400

    try:
        new_user = User(
            username=data.get('username'),
            email=data.get('email'),
            password=generate_password_hash(data.get('password')),
            notification_preference=data.get('notification_preference', None) # Because it is nullable
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to create user', 'error': str(e)}), 500

# Get the logged-in user's profile details
@user_bp.route('/users', methods=['GET'])
def get_user_profile():
    user, error_response, status_code = verify_user() # Verify user's existence and login before action
    if error_response:
        return error_response, status_code

    return jsonify(user_schema.dump(user)), 200
    
# Update the logged-in user's details
# (Password isn't updated here. Check the next route)
@user_bp.route('/users', methods=['PUT'])
def update_user():
    user, error_response, status_code = verify_user()
    if error_response:
        return error_response, status_code

    data = request.json
    # Update user details from request body
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'notification_preference' in data:
        user.notification_preference = data['notification_preference']

    try:
        db.session.commit()

        return jsonify({'message': 'User updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update user', 'error': str(e)}), 500

# Update the logged-in user's password
# (Was separated because it needs more checks)
@user_bp.route('/users/password', methods=['PUT'])
def update_password():
    user, error_response, status_code = verify_user()
    if error_response:
        return error_response, status_code

    data = request.json
    if 'current_password' not in data:
        return jsonify({'error': 'Current password is required'}), 400
    if 'new_password' not in data:
        return jsonify({'error': 'New password is required'}), 400
    current_password = data.get('current_password')
    new_password = data.get('new_password')

    # Verify the current password
    if not check_password_hash(user.password, current_password):
        return jsonify({'error': 'Current password is incorrect'}), 401
    
    if len(data.get('new_password')) < 8:
        return jsonify({'error': 'Password should be at least 8 characters long'}), 400

    # Hash and update the new password
    user.password = generate_password_hash(new_password)
    try:
        db.session.commit()

        return jsonify({'message': 'Password updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update user password', 'error': str(e)}), 500

# Delete the logged-in user's account
@user_bp.route('/users', methods=['DELETE'])
def delete_user():
    user, error_response, status_code = verify_user()
    if error_response:
        return error_response, status_code
    
    # Retrieve the confirmation flag from the request body
    confirm_delete = request.json.get('confirm_delete', False)

    # Check if the user has confirmed the deletion
    if not confirm_delete:
        return jsonify({'error': 'Account deletion not confirmed'}), 400

    try:
        # Delete the user and their associated tasks and reminders
        db.session.delete(user)
        db.session.commit()

        session.clear()  # Clear the user's session after deletion

        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to delete user', 'error': str(e)}), 500

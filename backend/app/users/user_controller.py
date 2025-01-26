from flask import Blueprint, request, jsonify
from app.users.models import User

# Create a blueprint for user-related routes
user_bp = Blueprint('user_controller', __name__, url_prefix='/api/users')

# Endpoint to create a new user
@user_bp.route('/', methods=['POST'])
def create_user():
    """
    Creates a new user based on the provided JSON data in the request body.

    The request body must include 'name', 'email', and 'password'.
    Optionally, the 'roles' field can be provided (default is ['USER']).

    Returns:
        - 400: If required fields are missing or if the email is already in use.
        - 201: If the user is successfully created, returns the user's details.
    """
    data = request.get_json()
    # Check if required fields are present in the request body
    if not data or not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400

    # Check if the email is already registered
    existing_user = User.get_user_by_email(data['email'])
    if existing_user:
        return jsonify({'error': 'Email already in use'}), 400
    
    # Create a new user
    user = User.create_user(
        name=data['name'],
        email=data['email'],
        password=data['password'],
        roles=data.get('roles', ['USER'])  # Default role is 'USER' if no roles are provided
    )
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'roles': user.get_roles()
    }), 201

# Endpoint to get a user by ID
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Retrieves a user by their ID.

    Returns:
        - 404: If the user with the specified ID is not found.
        - 200: Returns the user details.
    """
    user = User.get_user_by_id(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'roles': user.get_roles()
    })

# Endpoint to update a user by ID
@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Updates a user's details based on the provided JSON data.

    Fields that can be updated: 'name', 'email', 'password', 'roles'.

    Returns:
        - 404: If the user with the specified ID is not found.
        - 200: If the user is successfully updated.
    """
    data = request.get_json()
    user = User.get_user_by_id(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    
    # Update the user's fields
    updated_user = user.update_user(
        name=data.get('name', user.name),
        email=data.get('email', user.email),
        password=data.get('password', user.password),
        roles=data.get('roles', user.get_roles())
    )
    return jsonify({
        'message': 'User updated successfully',
        'user': {
            'id': updated_user.id,
            'name': updated_user.name,
            'email': updated_user.email,
            'roles': updated_user.get_roles()
        }
    })

# Endpoint to delete a user by ID
@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes a user by their ID.

    Returns:
        - 404: If the user with the specified ID is not found.
        - 200: If the user is successfully deleted.
    """
    success = User.delete_user(user_id)
    if not success:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'message': 'User deleted successfully'}), 200

# Endpoint to get all users
@user_bp.route('/', methods=['GET'])
def get_all_users():
    """
    Retrieves a list of all users.

    Returns:
        - 404: If no users are found.
        - 200: Returns a list of users.
    """
    users = User.get_all_users()  # Retrieve all users from the database
    if not users:
        return jsonify({'error': 'No users found'}), 404
    
    # Format the response with a list of users
    users_list = []
    for user in users:
        users_list.append({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'roles': user.get_roles()
        })
    
    return jsonify(users_list), 200

from flask import Blueprint, request, jsonify
from app.client.models import Client

client_bp = Blueprint('client_controller', __name__, url_prefix='/api/clients')

# Create a new client
@client_bp.route('/', methods=['POST'])
def create_client():
    """
    Create a new client.

    Expected request body:
    {
        "name": "Client Name",
        "email": "client@example.com"
    }

    Returns:
        JSON: The created client's data or an error message if any required field is missing.
    """
    data = request.get_json()
    if not data or not data.get('name') or not data.get('email'):
        return jsonify({'error': 'Missing required fields'}), 400

    # Check if email is already registered
    existing_client = Client.query.filter_by(email=data['email']).first()
    if existing_client:
        return jsonify({'error': 'Email already in use'}), 400

    client = Client.create_client(name=data['name'], email=data['email'])
    return jsonify({
        'id': client.id,
        'name': client.name,
        'email': client.email
    }), 201

# Get a client by ID
@client_bp.route('/<int:client_id>', methods=['GET'])
def get_client(client_id):
    """
    Get a client by their ID.

    Returns:
        JSON: The client's data or an error message if the client is not found.
    """
    client = Client.get_client_by_id(client_id)
    if client is None:
        return jsonify({'error': 'Client not found'}), 404
    return jsonify({
        'id': client.id,
        'name': client.name,
        'email': client.email
    })

# Get all clients
@client_bp.route('/', methods=['GET'])
def get_all_clients():
    """
    Get all clients.

    Returns:
        JSON: A list of all clients or an error message if no clients are found.
    """
    clients = Client.get_all_clients()
    if not clients:
        return jsonify({'error': 'No clients found'}), 404

    clients_list = []
    for client in clients:
        clients_list.append({
            'id': client.id,
            'name': client.name,
            'email': client.email
        })

    return jsonify(clients_list), 200

# Update a client
@client_bp.route('/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    """
    Update a client's details.

    Expected request body:
    {
        "name": "Updated Name",
        "email": "updated_email@example.com"
    }

    Returns:
        JSON: The updated client's data or an error message if the client is not found.
    """
    data = request.get_json()
    client = Client.get_client_by_id(client_id)
    if client is None:
        return jsonify({'error': 'Client not found'}), 404

    updated_client = client.update_client(
        name=data.get('name', client.name),
        email=data.get('email', client.email)
    )
    return jsonify({
        'message': 'Client updated successfully',
        'client': {
            'id': updated_client.id,
            'name': updated_client.name,
            'email': updated_client.email
        }
    })

# Delete a client
@client_bp.route('/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    """
    Delete a client by their ID.

    Returns:
        JSON: A success message or an error message if the client is not found.
    """
    success = Client.delete_client(client_id)
    if not success:
        return jsonify({'error': 'Client not found'}), 404
    return jsonify({'message': 'Client deleted successfully'}), 200

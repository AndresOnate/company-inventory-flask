from flask import Blueprint, request, jsonify
from app.client.models import Client

client_bp = Blueprint('client_controller', __name__, url_prefix='/api/clients')

# Crear un nuevo cliente
@client_bp.route('/', methods=['POST'])
def create_client():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('email'):
        return jsonify({'error': 'Missing required fields'}), 400

    # Verifica si el correo ya está registrado
    existing_client = Client.query.filter_by(email=data['email']).first()
    if existing_client:
        return jsonify({'error': 'Email already in use'}), 400

    client = Client.create_client(name=data['name'], email=data['email'])
    return jsonify({
        'id': client.id,
        'name': client.name,
        'email': client.email
    }), 201

# Obtener un cliente por ID
@client_bp.route('/<int:client_id>', methods=['GET'])
def get_client(client_id):
    client = Client.get_client_by_id(client_id)
    if client is None:
        return jsonify({'error': 'Client not found'}), 404
    return jsonify({
        'id': client.id,
        'name': client.name,
        'email': client.email
    })

# Obtener todos los clientes
@client_bp.route('/', methods=['GET'])
def get_all_clients():
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

# Actualizar un cliente
@client_bp.route('/<int:client_id>', methods=['PUT'])
def update_client(client_id):
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

# Eliminar un cliente
@client_bp.route('/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    success = Client.delete_client(client_id)
    if not success:
        return jsonify({'error': 'Client not found'}), 404
    return jsonify({'message': 'Client deleted successfully'}), 200

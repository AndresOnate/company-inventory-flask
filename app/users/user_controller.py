from flask import Blueprint, request, jsonify
from app.users.models import User

user_bp = Blueprint('user_controller', __name__, url_prefix='/api/users')

# Crear un nuevo usuario
@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400

    # Verifica si el correo ya está registrado
    existing_user = User.get_user_by_email(data['email'])
    if existing_user:
        return jsonify({'error': 'Email already in use'}), 400
    
    user = User.create_user(
        name=data['name'],
        email=data['email'],
        password=data['password'],
        roles=data.get('roles', ['USER'])  # Valor por defecto 'USER' si no se proporciona roles
    )
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'roles': user.get_roles()
    }), 201

# Obtener un usuario por ID
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.get_user_by_id(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'roles': user.get_roles()
    })

# Actualizar un usuario
@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.get_user_by_id(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    
    # Actualiza los campos del usuario
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

# Eliminar un usuario
@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    success = User.delete_user(user_id)
    if not success:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'message': 'User deleted successfully'}), 200

@user_bp.route('/', methods=['GET'])
def get_all_users():
    users = User.get_all_users()  # Método que obtendrá todos los usuarios de la base de datos
    if not users:
        return jsonify({'error': 'No users found'}), 404
    
    # Formato de respuesta con la lista de usuarios
    users_list = []
    for user in users:
        users_list.append({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'roles': user.get_roles()
        })
    
    return jsonify(users_list), 200
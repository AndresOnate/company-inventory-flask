from flask import Blueprint, request, jsonify
from app.category.models import Category

category_bp = Blueprint('category_controller', __name__, url_prefix='/api/categories')

# Crear una nueva categoría
@category_bp.route('/', methods=['POST'])
def create_category():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'Missing required field: name'}), 400

    category = Category.create_category(name=data['name'])
    return jsonify({
        'id': category.id,
        'name': category.name
    }), 201

# Obtener una categoría por ID
@category_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.get_category_by_id(category_id)
    if category is None:
        return jsonify({'error': 'Category not found'}), 404

    return jsonify({
        'id': category.id,
        'name': category.name
    })

# Actualizar una categoría
@category_bp.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    data = request.get_json()
    category = Category.get_category_by_id(category_id)
    if category is None:
        return jsonify({'error': 'Category not found'}), 404

    updated_category = category.update_category(name=data.get('name'))
    return jsonify({
        'message': 'Category updated successfully',
        'category': {
            'id': updated_category.id,
            'name': updated_category.name
        }
    })

# Eliminar una categoría
@category_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    success = Category.delete_category(category_id)
    if not success:
        return jsonify({'error': 'Category not found'}), 404

    return jsonify({'message': 'Category deleted successfully'}), 200

# Obtener todas las categorías
@category_bp.route('/', methods=['GET'])
def get_all_categories():
    categories = Category.get_all_categories()
    if not categories:
        return jsonify({'error': 'No categories found'}), 404

    # Formato de respuesta con la lista de categorías
    categories_list = []
    for category in categories:
        categories_list.append({
            'id': category.id,
            'name': category.name
        })

    return jsonify(categories_list), 200

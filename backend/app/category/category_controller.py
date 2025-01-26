from flask import Blueprint, request, jsonify
from app.category.models import Category

# Blueprint configuration for category operations
category_bp = Blueprint('category_controller', __name__, url_prefix='/api/categories')

# Create a new category
@category_bp.route('/', methods=['POST'])
def create_category():
    """
    Endpoint to create a new category.

    Expects a JSON body with a 'name' field.

    Returns:
        JSON response with the newly created category's ID and name.
    """
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'Missing required field: name'}), 400

    category = Category.create_category(name=data['name'])
    return jsonify({
        'id': category.id,
        'name': category.name
    }), 201

# Get a category by ID
@category_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """
    Endpoint to retrieve a category by its ID.

    Args:
        category_id (int): The ID of the category to retrieve.

    Returns:
        JSON response with the category details if found.
        Returns 404 if the category is not found.
    """
    category = Category.get_category_by_id(category_id)
    if category is None:
        return jsonify({'error': 'Category not found'}), 404

    return jsonify({
        'id': category.id,
        'name': category.name
    })

# Update a category
@category_bp.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    """
    Endpoint to update an existing category's name.

    Args:
        category_id (int): The ID of the category to update.

    Returns:
        JSON response with the updated category's details.
        Returns 404 if the category is not found.
    """
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

# Delete a category
@category_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    """
    Endpoint to delete a category by its ID.

    Args:
        category_id (int): The ID of the category to delete.

    Returns:
        JSON response confirming the deletion.
        Returns 404 if the category is not found.
    """
    success = Category.delete_category(category_id)
    if not success:
        return jsonify({'error': 'Category not found'}), 404

    return jsonify({'message': 'Category deleted successfully'}), 200

# Get all categories
@category_bp.route('/', methods=['GET'])
def get_all_categories():
    """
    Endpoint to retrieve all categories.

    Returns:
        JSON response with a list of all categories.
        Returns 404 if no categories are found.
    """
    categories = Category.get_all_categories()
    if not categories:
        return jsonify({'error': 'No categories found'}), 404

    # Format response with a list of categories
    categories_list = []
    for category in categories:
        categories_list.append({
            'id': category.id,
            'name': category.name
        })

    return jsonify(categories_list), 200

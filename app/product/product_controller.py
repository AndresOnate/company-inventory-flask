from flask import Blueprint, request, jsonify
from app.product.models import Product

product_bp = Blueprint('product_controller', __name__, url_prefix='/api/products')

# Crear un nuevo producto
@product_bp.route('/', methods=['POST'])
def create_product():
    data = request.get_json()
    if not data or not data.get('code') or not data.get('name') or not data.get('price') or not data.get('quantity'):
        return jsonify({'error': 'Missing required fields (code, name, price, quantity)'}), 400

    product = Product.create_product(
        code=data['code'],
        name=data['name'],
        description=data.get('description'),
        price=data['price'],
        quantity=data['quantity'],
        company_nit=data.get('company_nit')  # O puedes pasarla como una relación al crear el producto
    )
    return jsonify({
        'id': product.id,
        'code': product.code,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'quantity': product.quantity,
        'company_nit': product.company_nit,
        'company_name': product.company.name
    }), 201

# Obtener todos los productos
@product_bp.route('/', methods=['GET'])
def get_all_products():
    products = Product.get_all_products()
    if not products:
        return jsonify({'error': 'No products found'}), 404

    products_list = [{
        'id': product.id,
        'code': product.code,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'quantity': product.quantity,
        'company_nit': product.company_nit,
        'company_name': product.company.name
    } for product in products]

    return jsonify(products_list), 200

# Obtener un producto por ID
@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.get_product_by_id(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    return jsonify({
        'id': product.id,
        'code': product.code,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'quantity': product.quantity,
        'company_nit': product.company_nit,
        'company_name': product.company.name
    })

# Actualizar un producto
@product_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    product = Product.get_product_by_id(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    updated_product = product.update_product(
        code=data.get('code'),
        name=data.get('name'),
        description=data.get('description'),
        price=data.get('price'),
        quantity=data.get('quantity'),
        company_nit=data.get('company_nit')
    )

    return jsonify({
        'id': updated_product.id,
        'code': updated_product.code,
        'name': updated_product.name,
        'description': updated_product.description,
        'price': updated_product.price,
        'quantity': updated_product.quantity,
        'company_nit': updated_product.company_nit,
        'company_name': updated_product.company.name
    })

# Eliminar un producto
@product_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    success = Product.delete_product(product_id)
    if not success:
        return jsonify({'error': 'Product not found'}), 404

    return jsonify({'message': 'Product deleted successfully'}), 200

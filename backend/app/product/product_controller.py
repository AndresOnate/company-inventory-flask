from flask import Blueprint, request, jsonify
from app.product.models import Product

# Creating a Blueprint for product-related API routes
product_bp = Blueprint('product_controller', __name__, url_prefix='/api/products')

# Route to create a new product
@product_bp.route('/', methods=['POST'])
def create_product():
    """
    Creates a new product by accepting data from the request body.
    
    Expected data fields:
        - code: Product code (required)
        - name: Product name (required)
        - price: Product price (required)
        - quantity: Available product quantity (required)
        - description: Product description (optional)
        - company_nit: Company NIT (optional)
    
    Returns:
        - A JSON response containing the created product's details.
        - Status code 201 if successful, 400 if required fields are missing.
    """
    data = request.get_json()
    
    # Check if all required fields are present
    if not data or not data.get('code') or not data.get('name') or not data.get('price') or not data.get('quantity'):
        return jsonify({'error': 'Missing required fields (code, name, price, quantity)'}), 400

    # Create the product in the database
    product = Product.create_product(
        code=data['code'],
        name=data['name'],
        description=data.get('description'),
        price=data['price'],
        quantity=data['quantity'],
        company_nit=data.get('company_nit')  # This can be passed as a relationship when creating the product
    )
    
    # Return a response with the newly created product's details
    return jsonify({
        'id': product.id,
        'code': product.code,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'quantity': product.quantity,
        'company_nit': product.company_nit,
        'company_name': product.company.name  # Get the company name via the company relationship
    }), 201

# Route to get all products
@product_bp.route('/', methods=['GET'])
def get_all_products():
    """
    Retrieves all products from the database and returns them as a list.
    
    Returns:
        - A JSON response containing a list of all products.
        - Status code 200 if successful, 404 if no products are found.
    """
    products = Product.get_all_products()
    
    # If no products are found, return an error message
    if not products:
        return jsonify({'error': 'No products found'}), 404

    # Prepare a list of products with their details
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

    # Return a JSON response containing the list of products
    return jsonify(products_list), 200

# Route to get a product by its ID
@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    Retrieves a single product from the database based on its ID.
    
    Args:
        product_id (int): The ID of the product to retrieve.
    
    Returns:
        - A JSON response containing the product's details.
        - Status code 200 if successful, 404 if the product is not found.
    """
    product = Product.get_product_by_id(product_id)
    
    # If the product is not found, return an error message
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    # Return the product details in the response
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

# Route to update a product's details
@product_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """
    Updates the details of an existing product.
    
    Args:
        product_id (int): The ID of the product to update.
    
    Expected data fields:
        - code: Product code (optional)
        - name: Product name (optional)
        - description: Product description (optional)
        - price: Product price (optional)
        - quantity: Available product quantity (optional)
        - company_nit: Company NIT (optional)
    
    Returns:
        - A JSON response containing the updated product's details.
        - Status code 200 if successful, 404 if the product is not found.
    """
    data = request.get_json()
    
    # Retrieve the product by its ID
    product = Product.get_product_by_id(product_id)
    
    # If the product is not found, return an error message
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    # Update the product's details
    updated_product = product.update_product(
        code=data.get('code'),
        name=data.get('name'),
        description=data.get('description'),
        price=data.get('price'),
        quantity=data.get('quantity'),
        company_nit=data.get('company_nit')
    )

    # Return the updated product details
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

# Route to delete a product by its ID
@product_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """
    Deletes an existing product from the database.
    
    Args:
        product_id (int): The ID of the product to delete.
    
    Returns:
        - A JSON response indicating whether the deletion was successful.
        - Status code 200 if successful, 404 if the product is not found.
    """
    success = Product.delete_product(product_id)
    
    # If the product is not found, return an error message
    if not success:
        return jsonify({'error': 'Product not found'}), 404

    # Return a success message if the product was deleted
    return jsonify({'message': 'Product deleted successfully'}), 200

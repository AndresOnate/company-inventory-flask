from flask import Blueprint, request, jsonify
from app.company.models import Company
from app.order.models import Order
from app.product.models import Product

# Initialize the Blueprint for company routes
company_bp = Blueprint('company_controller', __name__, url_prefix='/api/companies')

# Create a new company
@company_bp.route('/', methods=['POST'])
def create_company():
    """
    Creates a new company with the provided data.
    Requires 'nit' and 'name' fields. If any are missing, an error is returned.
    If the NIT is already in use, an error is returned.
    """
    data = request.get_json()

    # Validate input data
    if not data or not data.get('nit') or not data.get('name'):
        return jsonify({'error': 'Missing required fields (nit, name)'}), 400

    # Check if the NIT is already registered
    existing_company = Company.get_company_by_nit(data['nit'])
    if existing_company:
        return jsonify({'error': 'NIT already in use'}), 400

    # Create the new company
    company = Company.create_company(
        nit=data['nit'],
        name=data['name'],
        address=data.get('address'),
        phone=data.get('phone')
    )
    return jsonify({
        'nit': company.nit,
        'name': company.name,
        'address': company.address,
        'phone': company.phone
    }), 201

# Get a company by NIT
@company_bp.route('/<string:nit>', methods=['GET'])
def get_company(nit):
    """
    Retrieves a company by its NIT.
    If the company does not exist, an error is returned.
    """
    company = Company.get_company_by_nit(nit)
    if not company:
        return jsonify({'error': 'Company not found'}), 404

    return jsonify({
        'nit': company.nit,
        'name': company.name,
        'address': company.address,
        'phone': company.phone
    })

# Get all companies
@company_bp.route('/', methods=['GET'])
def get_all_companies():
    """
    Retrieves all companies registered.
    If no companies exist, an error is returned.
    """
    companies = Company.get_all_companies()
    if not companies:
        return jsonify({'error': 'No companies found'}), 404

    companies_list = [{
        'nit': company.nit,
        'name': company.name,
        'address': company.address,
        'phone': company.phone
    } for company in companies]

    return jsonify(companies_list), 200

# Update a company
@company_bp.route('/<string:nit>', methods=['PUT'])
def update_company(nit):
    """
    Updates the details of a company.
    Updates the fields 'name', 'address', and 'phone'.
    If the company is not found, an error is returned.
    """
    data = request.get_json()
    company = Company.get_company_by_nit(nit)
    if not company:
        return jsonify({'error': 'Company not found'}), 404

    updated_company = company.update_company(
        name=data.get('name'),
        address=data.get('address'),
        phone=data.get('phone')
    )

    return jsonify({
        'message': 'Company updated successfully',
        'company': {
            'nit': updated_company.nit,
            'name': updated_company.name,
            'address': updated_company.address,
            'phone': updated_company.phone
        }
    })

# Delete a company
@company_bp.route('/<string:nit>', methods=['DELETE'])
def delete_company(nit):
    """
    Deletes a company by its NIT.
    If the company is not found, an error is returned.
    """
    success = Company.delete_company(nit)
    if not success:
        return jsonify({'error': 'Company not found'}), 404

    return jsonify({'message': 'Company deleted successfully'}), 200

# Create a new order for a company
@company_bp.route('/<string:nit>/orders', methods=['POST'])
def create_order_for_company(nit):
    """
    Creates a new order for a company specified by its NIT.
    Requires 'order_date' and 'client_id' fields. If missing, an error is returned.
    """
    data = request.get_json()
    if not data or not data.get('order_date') or not data.get('client_id'):
        return jsonify({'error': 'Missing required fields (order_date, client_id)'}), 400

    company = Company.get_company_by_nit(nit)
    if not company:
        return jsonify({'error': 'Company not found'}), 404

    order = Order.create_order(order_date=data['order_date'], client_id=data['client_id'])
    return jsonify({
        'id': order.id,
        'order_date': order.order_date,
        'client_id': order.client_id
    }), 201

# Get all orders for a company
@company_bp.route('/<string:nit>/orders', methods=['GET'])
def get_orders_for_company(nit):
    """
    Retrieves all orders associated with a company by its NIT.
    If the company does not exist, an error is returned.
    """
    company = Company.get_company_by_nit(nit)
    if not company:
        return jsonify({'error': 'Company not found'}), 404

    orders = company.products  # Assuming orders are indirectly related through products
    orders_list = [{
        'id': order.id,
        'order_date': order.order_date,
        'client_id': order.client_id
    } for order in orders]

    return jsonify(orders_list), 200

# Delete an order from a company
@company_bp.route('/<string:nit>/orders/<int:order_id>', methods=['DELETE'])
def delete_order_for_company(nit, order_id):
    """
    Deletes an order from a company by its NIT and order ID.
    If the company or the order is not found, an error is returned.
    """
    company = Company.get_company_by_nit(nit)
    if not company:
        return jsonify({'error': 'Company not found'}), 404

    order = Order.get_order_by_id(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    success = Order.delete_order(order_id)
    if not success:
        return jsonify({'error': 'Failed to delete order'}), 400

    return jsonify({'message': 'Order deleted successfully'}), 200

# Get products associated with a company
@company_bp.route('/<string:nit>/products', methods=['GET'])
def get_products_for_company(nit):
    """
    Retrieves all products associated with a company by its NIT.
    If the company does not exist, an error is returned.
    """
    company = Company.get_company_by_nit(nit)
    if not company:
        return jsonify({'error': 'Company not found'}), 404

    products = company.products  # Assuming products are directly associated
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

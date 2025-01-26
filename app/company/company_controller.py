from flask import Blueprint, request, jsonify
from app.company.models import Company
from app.order.models import Order
from app.product.models import Product

company_bp = Blueprint('company_controller', __name__, url_prefix='/api/companies')

# Crear una nueva empresa
@company_bp.route('/', methods=['POST'])
def create_company():
    data = request.get_json()
    if not data or not data.get('nit') or not data.get('name'):
        return jsonify({'error': 'Missing required fields (nit, name)'}), 400

    # Verificar si el NIT ya está registrado
    existing_company = Company.get_company_by_nit(data['nit'])
    if existing_company:
        return jsonify({'error': 'NIT already in use'}), 400

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

# Obtener una empresa por NIT
@company_bp.route('/<string:nit>', methods=['GET'])
def get_company(nit):
    company = Company.get_company_by_nit(nit)
    if not company:
        return jsonify({'error': 'Company not found'}), 404

    return jsonify({
        'nit': company.nit,
        'name': company.name,
        'address': company.address,
        'phone': company.phone
    })

# Obtener todas las empresas
@company_bp.route('/', methods=['GET'])
def get_all_companies():
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

# Actualizar una empresa
@company_bp.route('/<string:nit>', methods=['PUT'])
def update_company(nit):
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

# Eliminar una empresa
@company_bp.route('/<string:nit>', methods=['DELETE'])
def delete_company(nit):
    success = Company.delete_company(nit)
    if not success:
        return jsonify({'error': 'Company not found'}), 404

    return jsonify({'message': 'Company deleted successfully'}), 200

# Crear una nueva orden
@company_bp.route('/<string:nit>/orders', methods=['POST'])
def create_order_for_company(nit):
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

# Obtener todas las órdenes de una empresa
@company_bp.route('/<string:nit>/orders', methods=['GET'])
def get_orders_for_company(nit):
    company = Company.get_company_by_nit(nit)
    if not company:
        return jsonify({'error': 'Company not found'}), 404

    orders = company.products  # Suponiendo que las órdenes están relacionadas indirectamente a través de productos
    orders_list = [{
        'id': order.id,
        'order_date': order.order_date,
        'client_id': order.client_id
    } for order in orders]

    return jsonify(orders_list), 200

# Eliminar una orden de una empresa
@company_bp.route('/<string:nit>/orders/<int:order_id>', methods=['DELETE'])
def delete_order_for_company(nit, order_id):
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


@company_bp.route('/<string:nit>/products', methods=['GET'])
def get_products_for_company(nit):
    company = Company.get_company_by_nit(nit)
    if not company:
        return jsonify({'error': 'Company not found'}), 404

    products = company.products  # Suponiendo que las órdenes están relacionadas indirectamente a través de productos
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
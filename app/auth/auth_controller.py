from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
import jwt
from datetime import datetime, timedelta
from app.users.models import User
from app.exceptions.exceptions import InvalidCredentialsException
from app.users.models import RoleEnum


auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
SECRET_KEY = "2D4A614E645267556B58703273357638792F423F4428472B4B6250655368566D"


@auth_bp.route('', methods=['POST'])
def login():
    """
    Login endpoint where users can submit their email and password to authenticate.
    
    If the credentials are valid, a JWT token is generated and returned.
    Otherwise, an InvalidCredentialsException is raised.

    Returns:
        JSON response containing the JWT token and its expiration date.
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        token, expiration_date = generate_token(user)
        return jsonify({'token': token, 'expiration_date': expiration_date}), 200
    else:
        raise InvalidCredentialsException()

def generate_token(user):
    """
    Generates a JWT token for the authenticated user with an expiration date.

    Args:
        user (User): The authenticated user whose token is being generated.

    Returns:
        tuple: A tuple containing the JWT token and its expiration date (ISO format).
    """
    expiration_date = datetime.utcnow() + timedelta(minutes=10)
    token = jwt.encode(
        {
            'sub': user.email,  
            'roles': [user.roles],  
            'iat': datetime.utcnow(),  
            'exp': expiration_date 
        },
        SECRET_KEY,  
        algorithm='HS256'
    )
    return token, expiration_date.isoformat()

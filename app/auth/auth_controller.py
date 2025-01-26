from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
import jwt
from datetime import datetime, timedelta
from app.users.models import User
from app.exceptions.exceptions import InvalidCredentialsException
from app.users.models import RoleEnum

# Configuración
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
SECRET_KEY = "2D4A614E645267556B58703273357638792F423F4428472B4B6250655368566D"


@auth_bp.route('', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Buscar usuario en la base de datos
    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        token, expiration_date = generate_token(user)
        return jsonify({'token': token, 'expiration_date': expiration_date}), 200
    else:
        raise InvalidCredentialsException()


def generate_token(user):
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

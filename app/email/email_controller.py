from flask import Blueprint, request, jsonify
import boto3
import base64
from app.config import Config
from botocore.exceptions import BotoCoreError, ClientError

email_bp = Blueprint('email_controller', __name__, url_prefix='/api/email')
SES = boto3.client(
        'ses',
        region_name=Config.SES_REGION_NAME,
        aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
    )

sender = Config.SES_EMAIL_SOURCE

@email_bp.route('/send-email', methods=['POST'])
def send_email():
    try:
        # Procesar los datos enviados desde el cliente
        if 'file' not in request.files or 'email' not in request.form:
            return jsonify({'error': 'Missing email or file data'}), 400
        
        pdf_file = request.files['file']
        to_email = request.form['email']
        print(to_email)

        if not pdf_file or not to_email:
            return jsonify({'error': 'Invalid email or file data'}), 400

        # Leer el archivo PDF enviado por el cliente
        pdf_content = pdf_file.read()

        # Codificar el contenido del PDF en base64
        encoded_pdf = base64.b64encode(pdf_content).decode('utf-8')

        # Crear un mensaje MIME
        subject = "Reporte de Inventario"
        body_text = "Adjunto encontrarás el reporte de inventario en formato PDF."
        raw_email = f"""From: andrescamiloquimbayo@gmail.com
To: {to_email}
Subject: {subject}
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="NextPart"

--NextPart
Content-Type: text/plain; charset="UTF-8"
Content-Transfer-Encoding: 7bit

{body_text}

--NextPart
Content-Type: application/pdf; name="inventory_report.pdf"
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename="inventory_report.pdf"

{encoded_pdf}
--NextPart--"""

        # Enviar el correo usando SES
        response = SES.send_raw_email(
            Source=sender,
            Destinations=[to_email],
            RawMessage={'Data': raw_email}
        )
        return jsonify({'message': 'Email sent successfully', 'message_id': response['MessageId']}), 200

    except (BotoCoreError, ClientError) as error:
        print(error)
        return jsonify({'error': str(error)}), 500

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500
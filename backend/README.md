# Backend Flask - Sistema de Gestión Inventario

Este proyecto es el backend del Sistema de Gestión Empresarial, que expone una API para gestionar empresas, productos, usuarios, inventarios y autenticación.

## Tecnologías Utilizadas

- **Python**: Lenguaje principal para el desarrollo.
- **Flask**: Framework web utilizado para construir la API REST.
- **Flask-SQLAlchemy**: ORM para la gestión de la base de datos.
- **Flask-Migrate**: Para la gestión de migraciones.
- **PyJWT**: Manejo de tokens JWT para autenticación.
- **Flask-Mail**: Envío de correos electrónicos.
- **SQLite/MySQL/PostgreSQL**: Base de datos configurable.
- **Boto3**: SDK para integración con AWS (envío de PDFs por correo).

## Instalación

Sigue estos pasos para instalar y ejecutar el backend:

### Prerrequisitos

Asegúrate de tener instalado:

- **Python** (3.8 o superior)
- **pip** o **pipenv** para la gestión de paquetes
- **AWS CLI** (si usas servicios de AWS)

### Instrucciones

1. Clona el repositorio
   ```bash
   git clone https://github.com/AndresOnate/company-inventory-flask.git
   ```
2. Moverse al directorio
   ```bash
   cd company-inventory-flask/backend
   ```
3. Crea y activa un entorno virtual
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa: venv\Scripts\activate
     ```
4. Instala las dependencias
   ```bash
   pip install -r requirements.txt
   ```
5. Inicia el servidor
    ```bash
   flask run
   ```

## Endpoints Principales

### Autenticación
- **POST** `/auth/login`: Inicia sesión.

### Empresas
- **GET** `/api/companies/`: Lista todas las empresas.
- **POST** `/api/companies/`: Crea una nueva empresa.
- **PUT** `/api/companies/<id>`: Actualiza una empresa.
- **DELETE** `/api/companies/<id>`: Elimina una empresa.

### Productos
- **GET** `/api/products/`: Lista todos los productos.
- **POST** `/api/products/`: Crea un nuevo producto.
- **PUT** `/api/products/<id>`: Actualiza un producto.
- **DELETE** `/api/products/<id>`: Elimina un producto.

### Email
- **POST** `/api/email/send-email`: Genera y envía un PDF por correo.

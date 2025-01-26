# Frontend React - Sistema de Gestión Inventario

Este proyecto es la interfaz de usuario del Sistema de Gestión Empresarial. Permite a los usuarios interactuar con las vistas de empresas, productos, inventarios y autenticación.

## Tecnologías Utilizadas

- **React**: Framework principal para la construcción de la interfaz.
- **Axios**: Para manejar las solicitudes HTTP al backend.
- **React Router**: Para la navegación entre vistas.
- **Vite**: Como herramienta de construcción para un entorno de desarrollo rápido.

## Instalación

Sigue estos pasos para instalar y ejecutar el frontend:

### Prerrequisitos

Asegúrate de tener instalado:

- **Node.js** (v16 o superior)
- **npm** o **yarn**

### Instrucciones

1. Clona el repositorio
   ```bash
   git clone https://github.com/AndresOnate/company-inventory-flask.git
   ```
2. Moverse al directorio
   ```bash
   cd company-inventory-flask/frontend
   ```
3. Ejecuta el entorno de desarrollo Con npm:
    ```bash
       npm start
     ```

### Características
- Formulario de autenticación para inicio de sesión.
- Gestión de empresas con funcionalidades de creación, edición y eliminación.
- Visualización y registro de productos asociados a empresas.
- Generación y descarga de inventarios en formato PDF.
- Envío de PDFs por correo mediante integración con AWS.

# Sistema de Gestión Inventario

Este proyecto consiste en el desarrollo de una aplicación que gestiona empresas, productos e inventarios, incluyendo funcionalidades avanzadas como la generación y envío de PDFs, integración con AWS y soporte para diferentes roles de usuario.

## Funcionalidades Principales

### 1. Vista Empresa
Formulario que permite capturar la siguiente información:

![image](https://github.com/user-attachments/assets/10e4c08f-44e4-473a-b466-7f617383fbed)


### 2. Vista Productos
Formulario que permite capturar la siguiente información:

![image](https://github.com/user-attachments/assets/55c028c4-b5e8-47c9-9418-b24d6174786c)

### 3. Vista Inicio de Sesión
Formulario para la autenticación de usuarios con:

![image](https://github.com/user-attachments/assets/157df122-e80b-44cf-9c36-192e9243f4db)


### 4. Vista Inventario
- Formulario que permite la descarga de un PDF con la información de la tabla de inventario.
- Funcionalidad para enviar dicho PDF a un correo específico utilizando una API de AWS.

![image](https://github.com/user-attachments/assets/a3e88b67-31f7-4b71-a42c-43cfe4c8773b)

## Tipos de Usuario

### Administrador
- Acceso completo a las funcionalidades de eliminación, registro y edición de empresas.
- Capacidad para registrar productos asociados a una empresa.
- Gestión de inventarios con visualización de productos por empresa.

### Externo
- Permite la visualización de empresas como visitante.

## Modelo Entidad-Relación (ER)
El sistema utiliza un modelo de base de datos que incluye las siguientes entidades principales:
- **Empresa.**
- **Productos.**
- **Categorías.**
- **Clientes.**
- **Órdenes.**

### Requisitos del Modelo ER
1. Un **Producto** puede pertenecer a múltiples **Categorías**.
2. Un **Cliente** puede tener múltiples **Órdenes**.
3. Las **Órdenes** pueden contener múltiples **Productos**.

## Tecnologías Utilizadas
- **Backend:** Flask (Python).
- **Base de Datos:** Relacional (ej. PostgreSQL).
- **Frontend:** React, HTML, CSS, JavaScript.
- **PDF Generation:** ReportLab o similar.
- **Integración de AWS:** Envío de correos y manejo de archivos.


# Sistema de Gestión Inventario

Este proyecto consiste en el desarrollo de una aplicación que gestiona empresas, productos e inventarios, incluyendo funcionalidades avanzadas como la generación y envío de PDFs, integración con AWS y soporte para diferentes roles de usuario.

## Funcionalidades Principales

### 1. Vista Empresa
Formulario que permite capturar la siguiente información:
- **NIT:** Llave primaria.
- **Nombre de la empresa.**
- **Dirección.**
- **Teléfono.**

### 2. Vista Productos
Formulario que permite capturar la siguiente información:
- **Código.**
- **Nombre del producto.**
- **Características.**
- **Precio en varias monedas.**
- **Empresa asociada.**

### 3. Vista Inicio de Sesión
Formulario para la autenticación de usuarios con:
- **Correo electrónico.**
- **Contraseña.**

### 4. Vista Inventario
- Formulario que permite la descarga de un PDF con la información de la tabla de inventario.
- Funcionalidad para enviar dicho PDF a un correo específico utilizando una API de AWS.

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


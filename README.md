# flask-phone-shop

Este es un proyecto básico de Flask que incluye migraciones de base de datos con Flask-Migrate y consultas usando Flask-SQLAlchemy.

## Requisitos

- Python 3.x
- pip (gestor de paquetes de Python)
- MySQL (o cualquier otra base de datos compatible)

## Configuración del Entorno

1. **Instalar las dependencias:**
   ```bash
   pip install -r requierements.txt

2. **Inicializar el servidor:**
  Correr XAMPP o MAMP en la dirección del proyecto.

3. **Crear base de datos:**
  Ingresar a phpMyAdmin o desde la terminal y crear la base de datos con el nombre:
   ```bash
   flask_phone_shop

4. **Inicializar la base de datos y correr las migraciones:**
   ```bash
   flask db init
   flask db migrate -m "init migration"
   flask db upgrade


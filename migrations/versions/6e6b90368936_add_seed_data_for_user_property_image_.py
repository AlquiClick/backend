"""Add seed data for User, Property, Image, and Publication

Revision ID: 6e6b90368936
Revises: 4ddf548c5726
Create Date: 2024-11-02 18:59:43.146032

"""
from alembic import op
import sqlalchemy as sa
from datetime import date


# revision identifiers, used by Alembic.
revision = '6e6b90368936'
down_revision = '4ddf548c5726'
branch_labels = None
depends_on = None

def upgrade():
    op.bulk_insert(
        sa.table('person', sa.Column('id', sa.Integer), sa.Column('first_name', sa.String), sa.Column('last_name', sa.String), sa.Column('date_of_birth', sa.Date)),
        [
            {'id': 1, 'first_name': 'German', 'last_name': 'Lux', 'date_of_birth': '1998-07-22'},
            {'id': 2, 'first_name': 'Jose', 'last_name': 'Sand', 'date_of_birth': '1998-07-23'},
            {'id': 3, 'first_name': 'Jorge', 'last_name': 'Bermudez', 'date_of_birth': '1998-07-24'},
            {'id': 4, 'first_name': 'Miguel', 'last_name': 'Merentiel', 'date_of_birth': '1998-07-25'},
        ]
    )

    op.bulk_insert(
        sa.table('user', sa.Column('id', sa.Integer), sa.Column('username', sa.String), sa.Column('email', sa.String), sa.Column('person_id', sa.Integer), sa.Column('password', sa.String), sa.Column('is_active', sa.Boolean), sa.Column('is_admin', sa.Boolean)),
        [
            {'id': 1, 'username': 'admin', 'email': 'admin@example.com', 'person_id': 1, 'password': 'pbkdf2:sha256:600000$VFYEKesb$41c6afadd98adee4034ab1d9d15e69e4d4c4e7603c2adb7d12a9016ca5053a18', 'is_active': True, 'is_admin': True},
            {'id': 2, 'username': 'user1', 'email': 'user1@example.com', 'person_id': 2, 'password': 'pbkdf2:sha256:600000$VFYEKesb$41c6afadd98adee4034ab1d9d15e69e4d4c4e7603c2adb7d12a9016ca5053a18', 'is_active': True, 'is_admin': False},
            {'id': 3, 'username': 'user2', 'email': 'user2@example.com', 'person_id': 3, 'password': 'pbkdf2:sha256:600000$VFYEKesb$41c6afadd98adee4034ab1d9d15e69e4d4c4e7603c2adb7d12a9016ca5053a18', 'is_active': True, 'is_admin': False},
            {'id': 4, 'username': 'user3', 'email': 'user3@example.com', 'person_id': 4, 'password': 'pbkdf2:sha256:600000$VFYEKesb$41c6afadd98adee4034ab1d9d15e69e4d4c4e7603c2adb7d12a9016ca5053a18', 'is_active': True, 'is_admin': False},
        ]
    )

    # Insertar datos iniciales en Property
    op.bulk_insert(
        sa.table('property', sa.Column('id', sa.Integer), sa.Column('address', sa.String), sa.Column('rooms', sa.Integer), sa.Column('bathrooms', sa.Integer), sa.Column('garage_capacity', sa.Integer), sa.Column('year_built', sa.Integer), sa.Column('monthly_rent', sa.Numeric), sa.Column('owner_id', sa.Integer), sa.Column('active', sa.Boolean)),
        [
            {'id': 1, 'address': '123 Main St', 'rooms': 3, 'bathrooms': 2, 'garage_capacity': 1, 'year_built': 2000, 'monthly_rent': 1500.00, 'owner_id': 1, 'active': True},
            {'id': 2, 'address': '456 Elm St', 'rooms': 4, 'bathrooms': 3, 'garage_capacity': 2, 'year_built': 2010, 'monthly_rent': 2000.00, 'owner_id': 2, 'active': True},
            {'id': 3, 'address': '789 Maple St', 'rooms': 2, 'bathrooms': 1, 'garage_capacity': 1, 'year_built': 1995, 'monthly_rent': 1200.00, 'owner_id': 3, 'active': True},
            {'id': 4, 'address': '101 Oak St', 'rooms': 5, 'bathrooms': 4, 'garage_capacity': 2, 'year_built': 2015, 'monthly_rent': 2500.00, 'owner_id': 4, 'active': True},
        ]
    )


    op.bulk_insert(
        sa.table('image', sa.Column('id', sa.Integer), sa.Column('name', sa.String), sa.Column('url', sa.String)),
        [
            {'id': 1, 'name': 'Front View', 'url': 'http://example.com/front1.jpg'},
            {'id': 2, 'name': 'Back View', 'url': 'http://example.com/back1.jpg'},
            {'id': 3, 'name': 'Living Room', 'url': 'http://example.com/living_room1.jpg'},
            {'id': 4, 'name': 'Bedroom', 'url': 'http://example.com/bedroom1.jpg'},
        ]
    )

    op.bulk_insert(
        sa.table('publication', sa.Column('id', sa.Integer), sa.Column('property_id', sa.Integer), sa.Column('image_id', sa.Integer), sa.Column('user_id', sa.Integer), sa.Column('title', sa.String), sa.Column('description', sa.Text), sa.Column('price_shown', sa.Numeric), sa.Column('publication_status_id', sa.Integer), sa.Column('publish_date', sa.Date), sa.Column('expiry_date', sa.Date), sa.Column('status', sa.Enum)),
        [
            {'id': 1, 'property_id': 1, 'image_id': 1, 'user_id': 1, 'title': 'Charming Family Home', 'description': 'A beautiful family house with modern amenities.', 'price_shown': 1500.00, 'publication_status_id': 1, 'publish_date': date.today(), 'expiry_date': None, 'status': 'active'},
            {'id': 2, 'property_id': 2, 'image_id': 2, 'user_id': 2, 'title': 'Modern City Apartment', 'description': 'A stylish apartment in the heart of the city.', 'price_shown': 2000.00, 'publication_status_id': 1, 'publish_date': date.today(), 'expiry_date': None, 'status': 'active'},
            {'id': 3, 'property_id': 3, 'image_id': 3, 'user_id': 3, 'title': 'Cozy Bungalow', 'description': 'A cozy and affordable bungalow in a quiet neighborhood.', 'price_shown': 1200.00, 'publication_status_id': 1, 'publish_date': date.today(), 'expiry_date': None, 'status': 'active'},
            {'id': 4, 'property_id': 4, 'image_id': 4, 'user_id': 4, 'title': 'Luxury Villa', 'description': 'A luxurious villa with private pool and garden.', 'price_shown': 2500.00, 'publication_status_id': 1, 'publish_date': date.today(), 'expiry_date': None, 'status': 'active'},
        ]
    )

def downgrade():
    op.execute("DELETE FROM publication WHERE id BETWEEN 1 AND 4")
    op.execute("DELETE FROM image WHERE id BETWEEN 1 AND 4")
    op.execute("DELETE FROM property WHERE id BETWEEN 1 AND 4")
    op.execute("DELETE FROM user WHERE id BETWEEN 1 AND 4")
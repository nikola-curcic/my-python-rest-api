"""initial migration

Revision ID: f794c4d4f9b9
Revises: 
Create Date: 2019-11-05 10:40:39.008695

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f794c4d4f9b9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=True),
    sa.Column('password', sa.String(length=192), nullable=True),
    sa.Column('time_created', sa.String(length=25), nullable=True),
    sa.Column('user_level', sa.String(length=5), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vehicletypes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vehicle_type', sa.String(length=25), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('brands',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('id_vehicle_type', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_vehicle_type'], ['vehicletypes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('models',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('id_brand', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_brand'], ['brands.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('models')
    op.drop_table('brands')
    op.drop_table('vehicletypes')
    op.drop_table('users')
    # ### end Alembic commands ###
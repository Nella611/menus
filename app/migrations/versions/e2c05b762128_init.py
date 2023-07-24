"""init

Revision ID: e2c05b762128
Revises: 
Create Date: 2023-07-24 19:23:57.579687

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2c05b762128'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menus',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.Column('submenus_count', sa.Integer(), server_default='0', nullable=False),
    sa.Column('dishes_count', sa.Integer(), server_default='0', nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_menus_id'), 'menus', ['id'], unique=False)
    op.create_index(op.f('ix_menus_title'), 'menus', ['title'], unique=True)
    op.create_table('submenus',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('menu_id', sa.UUID(), nullable=True),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.Column('dishes_count', sa.Integer(), server_default='0', nullable=False),
    sa.ForeignKeyConstraint(['menu_id'], ['menus.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_submenus_id'), 'submenus', ['id'], unique=False)
    op.create_index(op.f('ix_submenus_title'), 'submenus', ['title'], unique=True)
    op.create_table('dishes',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('submenu_id', sa.UUID(), nullable=True),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.Column('price', sa.String(length=8), nullable=True),
    sa.ForeignKeyConstraint(['submenu_id'], ['submenus.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dishes_id'), 'dishes', ['id'], unique=False)
    op.create_index(op.f('ix_dishes_title'), 'dishes', ['title'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_dishes_title'), table_name='dishes')
    op.drop_index(op.f('ix_dishes_id'), table_name='dishes')
    op.drop_table('dishes')
    op.drop_index(op.f('ix_submenus_title'), table_name='submenus')
    op.drop_index(op.f('ix_submenus_id'), table_name='submenus')
    op.drop_table('submenus')
    op.drop_index(op.f('ix_menus_title'), table_name='menus')
    op.drop_index(op.f('ix_menus_id'), table_name='menus')
    op.drop_table('menus')
    # ### end Alembic commands ###

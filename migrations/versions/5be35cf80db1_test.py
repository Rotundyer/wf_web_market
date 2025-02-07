"""test

Revision ID: 5be35cf80db1
Revises: 
Create Date: 2024-06-03 02:54:17.926112

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '5be35cf80db1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('arcane_locations',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=True),
    sa.Column('name', sa.String(length=63), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('permission', sa.Integer(), nullable=False),
    sa.Column('id', sa.SmallInteger(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=31), nullable=False),
    sa.Column('permissions', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subtype_names',
    sa.Column('id', sa.SmallInteger(), autoincrement=True, nullable=False),
    sa.Column('tag', sa.String(length=31), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tag_names',
    sa.Column('id', sa.SmallInteger(), autoincrement=True, nullable=False),
    sa.Column('tag', sa.String(length=31), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('types',
    sa.Column('id', sa.SmallInteger(), autoincrement=True, nullable=False),
    sa.Column('type', sa.String(length=31), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('auth',
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('login', sa.String(length=31), nullable=False),
    sa.Column('hash_password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('registered_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('role', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['role'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('login')
    )
    op.create_index(op.f('ix_auth_id'), 'auth', ['id'], unique=False)
    op.create_table('items',
    sa.Column('wfm_id', sa.String(length=63), nullable=False),
    sa.Column('url_name', sa.String(length=63), nullable=False),
    sa.Column('trading_tax', sa.Integer(), nullable=True),
    sa.Column('icon', sa.String(length=255), nullable=True),
    sa.Column('type', sa.Integer(), nullable=False),
    sa.Column('item_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.ForeignKeyConstraint(['type'], ['types.id'], ),
    sa.PrimaryKeyConstraint('item_id'),
    sa.UniqueConstraint('url_name'),
    sa.UniqueConstraint('wfm_id')
    )
    op.create_index(op.f('ix_items_item_id'), 'items', ['item_id'], unique=False)
    op.create_table('arcanes',
    sa.Column('item_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('max_rank', sa.SmallInteger(), nullable=True),
    sa.Column('location', sa.SmallInteger(), nullable=True),
    sa.Column('vosfor', sa.SmallInteger(), nullable=True),
    sa.Column('reputation', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['items.item_id'], ),
    sa.PrimaryKeyConstraint('item_id')
    )
    op.create_index(op.f('ix_arcanes_item_id'), 'arcanes', ['item_id'], unique=False)
    op.create_table('items_update',
    sa.Column('item_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('wfm_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('url_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['items.item_id'], ),
    sa.ForeignKeyConstraint(['url_name'], ['items.url_name'], ),
    sa.ForeignKeyConstraint(['wfm_id'], ['items.wfm_id'], ),
    sa.PrimaryKeyConstraint('item_id'),
    sa.UniqueConstraint('url_name'),
    sa.UniqueConstraint('wfm_id')
    )
    op.create_index(op.f('ix_items_update_item_id'), 'items_update', ['item_id'], unique=False)
    op.create_table('l18n',
    sa.Column('item_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('language', sa.String(length=7), nullable=False),
    sa.Column('item_name', sa.String(length=255), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('wiki_link', sa.String(length=511), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['items.item_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mods',
    sa.Column('rarity', sa.String(length=63), nullable=True),
    sa.Column('mod_max_rank', sa.SmallInteger(), nullable=False),
    sa.Column('item_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['items.item_id'], ),
    sa.PrimaryKeyConstraint('item_id')
    )
    op.create_index(op.f('ix_mods_item_id'), 'mods', ['item_id'], unique=False)
    op.create_table('orders',
    sa.Column('order_id', sa.String(length=63), nullable=False),
    sa.Column('item_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('url_name', sa.String(length=63), nullable=False),
    sa.Column('platinum', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('order_type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('rank', sa.SmallInteger(), nullable=True),
    sa.Column('platform', sa.String(length=7), nullable=False),
    sa.Column('creation_date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('last_update', sa.DateTime(timezone=True), nullable=True),
    sa.Column('user_id', sa.String(length=63), nullable=True),
    sa.Column('user_ingame_name', sa.String(length=63), nullable=True),
    sa.Column('user_reputation', sa.SmallInteger(), nullable=True),
    sa.Column('user_last_seen', sa.DateTime(timezone=True), nullable=True),
    sa.Column('user_avatar', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['items.item_id'], ),
    sa.PrimaryKeyConstraint('order_id'),
    sa.UniqueConstraint('order_id')
    )
    op.create_table('relics',
    sa.Column('item_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('drops', sa.ARRAY(sa.UUID()), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['items.item_id'], ),
    sa.PrimaryKeyConstraint('item_id')
    )
    op.create_index(op.f('ix_relics_item_id'), 'relics', ['item_id'], unique=False)
    op.create_table('sculptures',
    sa.Column('item_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('amber_stars', sa.SmallInteger(), nullable=False),
    sa.Column('cyan_stars', sa.SmallInteger(), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['items.item_id'], ),
    sa.PrimaryKeyConstraint('item_id')
    )
    op.create_index(op.f('ix_sculptures_item_id'), 'sculptures', ['item_id'], unique=False)
    op.create_table('subtypes',
    sa.Column('item_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.SmallInteger(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['items.item_id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['subtype_names.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tags',
    sa.Column('item_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.SmallInteger(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['items.item_id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag_names.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('weapons',
    sa.Column('item_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('set_root', sa.Boolean(), nullable=False),
    sa.Column('main_root', sa.Boolean(), nullable=True),
    sa.Column('root_id', sa.ARRAY(sa.UUID()), nullable=True),
    sa.Column('quantity_for_set', sa.SmallInteger(), nullable=True),
    sa.Column('mastery_level', sa.SmallInteger(), nullable=True),
    sa.Column('ducats', sa.SmallInteger(), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['items.item_id'], ),
    sa.PrimaryKeyConstraint('item_id')
    )
    op.create_index(op.f('ix_weapons_item_id'), 'weapons', ['item_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_weapons_item_id'), table_name='weapons')
    op.drop_table('weapons')
    op.drop_table('tags')
    op.drop_table('subtypes')
    op.drop_index(op.f('ix_sculptures_item_id'), table_name='sculptures')
    op.drop_table('sculptures')
    op.drop_index(op.f('ix_relics_item_id'), table_name='relics')
    op.drop_table('relics')
    op.drop_table('orders')
    op.drop_index(op.f('ix_mods_item_id'), table_name='mods')
    op.drop_table('mods')
    op.drop_table('l18n')
    op.drop_index(op.f('ix_items_update_item_id'), table_name='items_update')
    op.drop_table('items_update')
    op.drop_index(op.f('ix_arcanes_item_id'), table_name='arcanes')
    op.drop_table('arcanes')
    op.drop_index(op.f('ix_items_item_id'), table_name='items')
    op.drop_table('items')
    op.drop_index(op.f('ix_auth_id'), table_name='auth')
    op.drop_table('auth')
    op.drop_table('types')
    op.drop_table('tag_names')
    op.drop_table('subtype_names')
    op.drop_table('roles')
    op.drop_table('arcane_locations')
    # ### end Alembic commands ###

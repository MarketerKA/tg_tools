"""empty message

Revision ID: 700f2b0fa662
Revises: 
Create Date: 2023-09-06 17:14:21.786331

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '700f2b0fa662'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tg_id', sa.String(), nullable=True),
    sa.Column('spammed', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_spammed'), 'users', ['spammed'], unique=False)
    op.create_index(op.f('ix_users_tg_id'), 'users', ['tg_id'], unique=False)
    op.create_table('users_base',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tg_id', sa.String(), nullable=True),
    sa.Column('tg_class', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_base_id'), 'users_base', ['id'], unique=False)
    op.create_index(op.f('ix_users_base_tg_class'), 'users_base', ['tg_class'], unique=False)
    op.create_index(op.f('ix_users_base_tg_id'), 'users_base', ['tg_id'], unique=False)
    op.create_table('workers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tg_id', sa.String(), nullable=True),
    sa.Column('time', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_workers_id'), 'workers', ['id'], unique=False)
    op.create_index(op.f('ix_workers_tg_id'), 'workers', ['tg_id'], unique=False)
    op.create_index(op.f('ix_workers_time'), 'workers', ['time'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_workers_time'), table_name='workers')
    op.drop_index(op.f('ix_workers_tg_id'), table_name='workers')
    op.drop_index(op.f('ix_workers_id'), table_name='workers')
    op.drop_table('workers')
    op.drop_index(op.f('ix_users_base_tg_id'), table_name='users_base')
    op.drop_index(op.f('ix_users_base_tg_class'), table_name='users_base')
    op.drop_index(op.f('ix_users_base_id'), table_name='users_base')
    op.drop_table('users_base')
    op.drop_index(op.f('ix_users_tg_id'), table_name='users')
    op.drop_index(op.f('ix_users_spammed'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
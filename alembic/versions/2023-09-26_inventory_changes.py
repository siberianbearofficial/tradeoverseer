"""inventory changes

Revision ID: 98e46f74b026
Revises: c5f0a98491a9
Create Date: 2023-09-26 15:17:14.939484

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '98e46f74b026'
down_revision: Union[str, None] = 'c5f0a98491a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('inventory')
    op.drop_column('user', 'inventory')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('inventory', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_table('inventory',
    sa.Column('uuid', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('skin_uuid', sa.UUID(), autoincrement=False, nullable=True),
    sa.Column('added_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('price', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('count', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['skin_uuid'], ['skin.uuid'], name='inventory_skin_uuid_fkey'),
    sa.PrimaryKeyConstraint('uuid', name='inventory_pkey')
    )
    # ### end Alembic commands ###

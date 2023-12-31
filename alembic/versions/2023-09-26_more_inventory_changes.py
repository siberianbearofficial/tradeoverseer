"""more inventory changes

Revision ID: 6a91a2c7d76a
Revises: 98e46f74b026
Create Date: 2023-09-26 15:20:46.791044

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a91a2c7d76a'
down_revision: Union[str, None] = '98e46f74b026'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('inventory',
    sa.Column('uuid', sa.Uuid(), nullable=False),
    sa.Column('user_uuid', sa.Uuid(), nullable=True),
    sa.Column('skin_uuid', sa.Uuid(), nullable=True),
    sa.Column('added_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('price', sa.String(), nullable=True),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['skin_uuid'], ['skin.uuid'], ),
    sa.ForeignKeyConstraint(['user_uuid'], ['user.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('inventory')
    # ### end Alembic commands ###

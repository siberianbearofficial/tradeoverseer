"""permissions json to str

Revision ID: c5f0a98491a9
Revises: 90bbcab31129
Create Date: 2023-09-25 16:13:33.514572

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c5f0a98491a9'
down_revision: Union[str, None] = '90bbcab31129'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('role', 'permissions',
               existing_type=postgresql.JSON(astext_type=sa.Text()),
               type_=sa.String(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('role', 'permissions',
               existing_type=sa.String(),
               type_=postgresql.JSON(astext_type=sa.Text()),
               existing_nullable=True)
    # ### end Alembic commands ###
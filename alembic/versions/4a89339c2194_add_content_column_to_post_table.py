"""add content column to post table


Revision ID: 4a89339c2194
Revises: d7029cbeae05
Create Date: 2023-08-30 20:26:06.352342

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a89339c2194'
down_revision: Union[str, None] = 'd7029cbeae05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable= False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')

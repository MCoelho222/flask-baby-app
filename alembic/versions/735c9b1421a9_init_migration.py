"""init migration

Revision ID: 735c9b1421a9
Revises:
Create Date: 2023-11-17 10:05:56.735869

"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '735c9b1421a9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'occurrence',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('type_tag', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('resume', sa.String(), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.Column('register_at', sa.DateTime(), nullable=False),
        sa.Column('update_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('occurrence')

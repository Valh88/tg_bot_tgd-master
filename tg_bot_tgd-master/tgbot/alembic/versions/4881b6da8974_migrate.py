"""migrate

Revision ID: 4881b6da8974
Revises: 8bc99ef81c8f
Create Date: 2023-03-04 17:40:06.422703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4881b6da8974'
down_revision = '8bc99ef81c8f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('language_code', sa.String(length=7), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'language_code')
    # ### end Alembic commands ###
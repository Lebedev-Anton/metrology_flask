"""add global_data in CheckedPoint

Revision ID: 0b7a8534f24f
Revises: 3271b78fb8ed
Create Date: 2022-01-27 23:00:21.881360

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b7a8534f24f'
down_revision = '3271b78fb8ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('checked_point', sa.Column('global_data', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('checked_point', 'global_data')
    # ### end Alembic commands ###

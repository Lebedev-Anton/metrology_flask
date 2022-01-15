"""add status

Revision ID: 4944da967468
Revises: 5f2fc34a7139
Create Date: 2022-01-14 23:37:21.270271

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4944da967468'
down_revision = '5f2fc34a7139'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('checked_point_data', sa.Column('status', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('checked_point_data', 'status')
    # ### end Alembic commands ###

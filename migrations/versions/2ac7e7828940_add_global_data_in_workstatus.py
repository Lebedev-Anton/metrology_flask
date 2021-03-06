"""add global_data in WorkStatus

Revision ID: 2ac7e7828940
Revises: 0b7a8534f24f
Create Date: 2022-01-27 23:16:21.136128

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ac7e7828940'
down_revision = '0b7a8534f24f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('checked_point', 'global_data')
    op.add_column('work_status', sa.Column('global_data', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('work_status', 'global_data')
    op.add_column('checked_point', sa.Column('global_data', sa.TEXT(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###

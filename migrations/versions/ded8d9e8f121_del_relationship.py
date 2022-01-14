"""del relationship

Revision ID: ded8d9e8f121
Revises: ad2e2c1e8674
Create Date: 2022-01-14 13:30:11.992799

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ded8d9e8f121'
down_revision = 'ad2e2c1e8674'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('checked_point_data', 'id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
    op.drop_constraint('unique_checked_point_data_id', 'checked_point_data', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('unique_checked_point_data_id', 'checked_point_data', ['id'])
    op.alter_column('checked_point_data', 'id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)
    # ### end Alembic commands ###
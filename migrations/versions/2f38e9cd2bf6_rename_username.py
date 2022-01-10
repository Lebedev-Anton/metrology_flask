"""rename username

Revision ID: 2f38e9cd2bf6
Revises: b64616543009
Create Date: 2022-01-10 15:08:41.541773

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f38e9cd2bf6'
down_revision = 'b64616543009'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.Text(), nullable=True))
    op.drop_index('ix_users_user_name', table_name='users')
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.drop_column('users', 'user_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('user_name', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.create_index('ix_users_user_name', 'users', ['user_name'], unique=False)
    op.drop_column('users', 'username')
    # ### end Alembic commands ###
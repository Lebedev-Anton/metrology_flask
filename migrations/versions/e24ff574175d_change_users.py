"""change Users 

Revision ID: e24ff574175d
Revises: 24613798e08c
Create Date: 2021-12-17 01:10:38.731955

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e24ff574175d'
down_revision = '24613798e08c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('post', sa.Text(), nullable=True))
    op.drop_index('ix_users_path', table_name='users')
    op.create_index(op.f('ix_users_post'), 'users', ['post'], unique=False)
    op.drop_column('users', 'path')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('path', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_users_post'), table_name='users')
    op.create_index('ix_users_path', 'users', ['path'], unique=False)
    op.drop_column('users', 'post')
    # ### end Alembic commands ###

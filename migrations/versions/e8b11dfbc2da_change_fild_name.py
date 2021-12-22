"""change fild name

Revision ID: e8b11dfbc2da
Revises: 7cff234ff2db
Create Date: 2021-12-23 01:31:59.126934

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e8b11dfbc2da'
down_revision = '7cff234ff2db'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_answer')
    op.drop_table('script_tree')
    op.drop_table('save_function_json')
    op.add_column('devices', sa.Column('serial_number', sa.Text(), nullable=True))
    op.add_column('devices', sa.Column('order_number', sa.Text(), nullable=True))
    op.add_column('devices', sa.Column('delivery_date', sa.DateTime(), nullable=True))
    op.drop_index('ix_devices_app_num', table_name='devices')
    op.drop_index('ix_devices_date', table_name='devices')
    op.drop_index('ix_devices_modification', table_name='devices')
    op.drop_index('ix_devices_ser_num', table_name='devices')
    op.create_index(op.f('ix_devices_order_number'), 'devices', ['order_number'], unique=False)
    op.create_index(op.f('ix_devices_serial_number'), 'devices', ['serial_number'], unique=False)
    op.drop_column('devices', 'date')
    op.drop_column('devices', 'app_num')
    op.drop_column('devices', 'ser_num')
    op.drop_index('ix_protocols_path', table_name='protocols')
    op.drop_index('ix_protocols_protocol_name', table_name='protocols')
    op.drop_index('ix_scripts_path', table_name='scripts')
    op.drop_index('ix_scripts_script_name', table_name='scripts')
    op.drop_column('scripts', 'path')
    op.drop_index('ix_user_data_base_name', table_name='user_data')
    op.drop_index('ix_user_data_path', table_name='user_data')
    op.add_column('users', sa.Column('employee_position', sa.Text(), nullable=True))
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_post', table_name='users')
    op.drop_column('users', 'post')
    op.drop_index('ix_work_status_work_status', table_name='work_status')
    op.drop_index('ix_work_type_work_type_name', table_name='work_type')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_work_type_work_type_name', 'work_type', ['work_type_name'], unique=False)
    op.create_index('ix_work_status_work_status', 'work_status', ['work_status'], unique=False)
    op.add_column('users', sa.Column('post', sa.TEXT(), autoincrement=False, nullable=True))
    op.create_index('ix_users_post', 'users', ['post'], unique=False)
    op.create_index('ix_users_email', 'users', ['email'], unique=False)
    op.drop_column('users', 'employee_position')
    op.create_index('ix_user_data_path', 'user_data', ['path'], unique=False)
    op.create_index('ix_user_data_base_name', 'user_data', ['base_name'], unique=False)
    op.add_column('scripts', sa.Column('path', sa.TEXT(), autoincrement=False, nullable=True))
    op.create_index('ix_scripts_script_name', 'scripts', ['script_name'], unique=False)
    op.create_index('ix_scripts_path', 'scripts', ['path'], unique=False)
    op.create_index('ix_protocols_protocol_name', 'protocols', ['protocol_name'], unique=False)
    op.create_index('ix_protocols_path', 'protocols', ['path'], unique=False)
    op.add_column('devices', sa.Column('ser_num', sa.TEXT(), autoincrement=False, nullable=True))
    op.add_column('devices', sa.Column('app_num', sa.TEXT(), autoincrement=False, nullable=True))
    op.add_column('devices', sa.Column('date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_devices_serial_number'), table_name='devices')
    op.drop_index(op.f('ix_devices_order_number'), table_name='devices')
    op.create_index('ix_devices_ser_num', 'devices', ['ser_num'], unique=False)
    op.create_index('ix_devices_modification', 'devices', ['modification'], unique=False)
    op.create_index('ix_devices_date', 'devices', ['date'], unique=False)
    op.create_index('ix_devices_app_num', 'devices', ['app_num'], unique=False)
    op.drop_column('devices', 'delivery_date')
    op.drop_column('devices', 'order_number')
    op.drop_column('devices', 'serial_number')
    op.create_table('save_function_json',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('work_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('json', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='save_function_json_pkey')
    )
    op.create_table('script_tree',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('work_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('function_name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('argument_of_function', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('current_point', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('next_point', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='script_tree_pkey')
    )
    op.create_table('user_answer',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('work_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_answer', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='user_answer_pkey')
    )
    # ### end Alembic commands ###

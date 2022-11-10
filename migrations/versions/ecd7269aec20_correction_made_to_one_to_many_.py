"""correction made to one to many relationship

Revision ID: ecd7269aec20
Revises: 7aa56264f17f
Create Date: 2022-11-09 20:51:18.206956

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ecd7269aec20'
down_revision = '7aa56264f17f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('goal_id', sa.Integer(), nullable=True))
    op.drop_constraint('task_task_id_fkey', 'task', type_='foreignkey')
    op.create_foreign_key(None, 'task', 'goal', ['goal_id'], ['id'])
    op.drop_column('task', 'task_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('task_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.create_foreign_key('task_task_id_fkey', 'task', 'task', ['task_id'], ['id'])
    op.drop_column('task', 'goal_id')
    # ### end Alembic commands ###

"""modified Goal model and added relationship with Task model

Revision ID: 4d11a8ad22a6
Revises: f70d5ed4e754
Create Date: 2022-11-08 19:38:07.847577

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d11a8ad22a6'
down_revision = 'f70d5ed4e754'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))
    op.drop_column('goal', 'goal_id')
    op.drop_constraint('task_goal_id_fkey', 'task', type_='foreignkey')
    op.create_foreign_key(None, 'task', 'goal', ['goal_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.create_foreign_key('task_goal_id_fkey', 'task', 'goal', ['goal_id'], ['goal_id'])
    op.add_column('goal', sa.Column('goal_id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_column('goal', 'id')
    # ### end Alembic commands ###

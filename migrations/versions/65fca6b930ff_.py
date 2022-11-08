"""empty message

Revision ID: 65fca6b930ff
Revises: 5b022f5099ee
Create Date: 2022-11-03 21:32:04.485602

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65fca6b930ff'
down_revision = '5b022f5099ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('task_goal_id_fkey', 'task', type_='foreignkey')
    op.drop_column('task', 'goal_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('goal_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('task_goal_id_fkey', 'task', 'goal', ['goal_id'], ['goal_id'])
    # ### end Alembic commands ###

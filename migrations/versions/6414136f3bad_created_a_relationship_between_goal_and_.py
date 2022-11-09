"""created a relationship between goal and task

Revision ID: 6414136f3bad
Revises: c8ae27ecd944
Create Date: 2022-11-08 10:34:35.688120

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6414136f3bad'
down_revision = 'c8ae27ecd944'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('goal_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'task', 'goal', ['goal_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.drop_column('task', 'goal_id')
    # ### end Alembic commands ###

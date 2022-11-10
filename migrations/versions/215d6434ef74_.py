"""empty message

Revision ID: 215d6434ef74
Revises: 1cd471221364
Create Date: 2022-11-09 15:16:13.743369

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '215d6434ef74'
down_revision = '1cd471221364'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('goal_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'task', 'goal', ['goal_id'], ['goal_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.drop_column('task', 'goal_id')
    # ### end Alembic commands ###

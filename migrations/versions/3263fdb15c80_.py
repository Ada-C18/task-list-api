"""empty message

Revision ID: 3263fdb15c80
Revises: 0d0a4c6d3af9
Create Date: 2022-11-08 15:07:26.289479

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3263fdb15c80'
down_revision = '0d0a4c6d3af9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('id', sa.Integer(), nullable=False))
    op.drop_column('task', 'task_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('task_id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_column('task', 'id')
    # ### end Alembic commands ###

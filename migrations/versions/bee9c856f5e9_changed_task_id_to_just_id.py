"""changed task_id to just id

Revision ID: bee9c856f5e9
Revises: c9d7da9a064d
Create Date: 2022-11-03 20:10:20.343201

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bee9c856f5e9'
down_revision = 'c9d7da9a064d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))
    op.drop_column('task', 'task_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('task_id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_column('task', 'id')
    # ### end Alembic commands ###

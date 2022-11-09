"""empty message

Revision ID: 33aefd39ecf8
Revises: 0c2ee9658802
Create Date: 2022-11-08 16:31:37.964436

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33aefd39ecf8'
down_revision = '0c2ee9658802'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('task_ids', sa.ARRAY(sa.Integer()), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('goal', 'task_ids')
    # ### end Alembic commands ###

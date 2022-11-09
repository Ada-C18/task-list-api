"""empty message

Revision ID: a5c7caef715a
Revises: 2dd636b1570b
Create Date: 2022-11-09 14:15:58.074060

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a5c7caef715a'
down_revision = '2dd636b1570b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('goal', 'task_ids')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('task_ids', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    # ### end Alembic commands ###

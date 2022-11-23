"""empty message

Revision ID: 046fe45b5bee
Revises: 3aac88f2cf1e
Create Date: 2022-11-06 01:45:06.204448

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '046fe45b5bee'
down_revision = '3aac88f2cf1e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('title', sa.String(), nullable=True))
    op.alter_column('task', 'completed_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('task', 'completed_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.drop_column('goal', 'title')
    # ### end Alembic commands ###

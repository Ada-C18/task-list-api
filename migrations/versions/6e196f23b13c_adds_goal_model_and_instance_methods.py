"""Adds goal model and instance methods

Revision ID: 6e196f23b13c
Revises: 8c1d59cc2afe
Create Date: 2022-11-09 13:43:19.336031

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e196f23b13c'
down_revision = '8c1d59cc2afe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('title', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('goal', 'title')
    # ### end Alembic commands ###

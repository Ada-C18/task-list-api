"""added title column to Goal

Revision ID: ccd5c4df1dd7
Revises: 23f7f42ca3eb
Create Date: 2022-11-07 14:09:15.638081

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccd5c4df1dd7'
down_revision = '23f7f42ca3eb'
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

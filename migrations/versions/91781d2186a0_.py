"""empty message

Revision ID: 91781d2186a0
Revises: 32deb148cb68
Create Date: 2022-11-08 10:38:33.779115

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91781d2186a0'
down_revision = '32deb148cb68'
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

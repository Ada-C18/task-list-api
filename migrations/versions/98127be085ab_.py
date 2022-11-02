"""empty message

Revision ID: 98127be085ab
Revises: 94d3665f7529
Create Date: 2022-11-02 15:00:11.129961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98127be085ab'
down_revision = '94d3665f7529'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('is_complete', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task', 'is_complete')
    # ### end Alembic commands ###

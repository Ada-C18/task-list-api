"""empty message

Revision ID: 3752cc9ac8cb
Revises: da51b29e1234
Create Date: 2022-11-02 17:54:11.705565

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3752cc9ac8cb'
down_revision = 'da51b29e1234'
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

"""empty message

Revision ID: ba5009c27a11
Revises: d442211d12a7
Create Date: 2022-11-02 16:09:10.692891

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba5009c27a11'
down_revision = 'd442211d12a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('completed_at', sa.DateTime(), nullable=True))
    op.add_column('task', sa.Column('description', sa.String(), nullable=True))
    op.add_column('task', sa.Column('title', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task', 'title')
    op.drop_column('task', 'description')
    op.drop_column('task', 'completed_at')
    # ### end Alembic commands ###

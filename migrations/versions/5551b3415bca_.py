"""empty message

Revision ID: 5551b3415bca
Revises: 91d304e19eb9
Create Date: 2022-11-03 22:58:02.897310

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5551b3415bca'
down_revision = '91d304e19eb9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('is_complete', sa.Boolean(), nullable=True))
    op.drop_column('task', 'is_completed')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('is_completed', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('task', 'is_complete')
    # ### end Alembic commands ###

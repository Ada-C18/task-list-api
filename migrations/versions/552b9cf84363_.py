"""empty message

Revision ID: 552b9cf84363
Revises: fef0f508dd24
Create Date: 2022-11-02 14:56:45.821224

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '552b9cf84363'
down_revision = 'fef0f508dd24'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('completed_at', sa.DateTime(), nullable=True))
    op.drop_column('task', 'is_complete')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('is_complete', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('task', 'completed_at')
    # ### end Alembic commands ###

"""empty message

Revision ID: f7651e896dd2
Revises: cd32ae4bc203
Create Date: 2022-11-07 21:09:08.064488

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f7651e896dd2'
down_revision = 'cd32ae4bc203'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('complete_at', sa.DateTime(), nullable=True))
    op.drop_column('task', 'completed_at')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('completed_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('task', 'complete_at')
    # ### end Alembic commands ###

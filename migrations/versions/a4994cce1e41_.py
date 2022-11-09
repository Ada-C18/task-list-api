"""empty message

Revision ID: a4994cce1e41
Revises: 2b6ac4497881
Create Date: 2022-11-09 10:04:08.547590

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4994cce1e41'
down_revision = '2b6ac4497881'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('text', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('goal', 'text')
    # ### end Alembic commands ###

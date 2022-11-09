"""empty message

Revision ID: 22b8cb72cb89
Revises: 52b95577b20d
Create Date: 2022-11-08 16:45:45.592669

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22b8cb72cb89'
down_revision = '52b95577b20d'
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

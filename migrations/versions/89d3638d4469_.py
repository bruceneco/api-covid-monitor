"""empty message

Revision ID: 89d3638d4469
Revises: b9badd85c082
Create Date: 2021-10-24 23:34:20.699899

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89d3638d4469'
down_revision = 'b9badd85c082'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('permission', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'permission')
    # ### end Alembic commands ###

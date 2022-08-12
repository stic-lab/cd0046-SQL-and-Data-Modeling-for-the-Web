"""empty message

Revision ID: 2621ce00c2e5
Revises: 2078081d182d
Create Date: 2022-08-12 16:17:06.856411

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2621ce00c2e5'
down_revision = '2078081d182d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artist_availability',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=True),
    sa.Column('begin_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('artist_availability')
    # ### end Alembic commands ###

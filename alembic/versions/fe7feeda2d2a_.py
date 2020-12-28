"""empty message

Revision ID: fe7feeda2d2a
Revises: 
Create Date: 2020-12-29 00:05:58.333047

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe7feeda2d2a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('app_id_in_appfigures', sa.BigInteger(), nullable=False),
    sa.Column('app_id_in_store', sa.String(length=50), nullable=False),
    sa.Column('game_name', sa.String(length=50), nullable=False),
    sa.Column('id_store', sa.SmallInteger(), nullable=False),
    sa.Column('store', sa.String(length=50), nullable=False),
    sa.Column('icon_link_appfigures', sa.String(length=2048), nullable=True),
    sa.Column('icon_link_s3', sa.String(length=2048), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('app_id_in_appfigures')
    )
    op.create_table('review',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('id_in_appfigures', sa.String(length=100), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('author', sa.String(length=100), nullable=False),
    sa.Column('pub_date', sa.DateTime(), nullable=False),
    sa.Column('stars', sa.Numeric(precision=3, scale=2), nullable=True),
    sa.Column('game_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_in_appfigures')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('review')
    op.drop_table('game')
    # ### end Alembic commands ###

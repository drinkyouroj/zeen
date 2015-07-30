"""Post content

Revision ID: 3a7ec0cd7b2
Revises: 56bc666ff2f
Create Date: 2015-07-29 19:38:19.259364

"""

# revision identifiers, used by Alembic.
revision = '3a7ec0cd7b2'
down_revision = '56bc666ff2f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_posts_timestamp', 'posts', ['timestamp'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_posts_timestamp', 'posts')
    op.drop_table('posts')
    ### end Alembic commands ###

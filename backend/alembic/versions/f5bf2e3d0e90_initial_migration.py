"""initial migration

Revision ID: f5bf2e3d0e90
Revises: 
Create Date: 2024-10-14 13:22:35.842920

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = 'f5bf2e3d0e90'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('link',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('url')
    )
    op.create_table('user_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('folder',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user_info.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('link_stat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('link_id', sa.Integer(), nullable=False),
    sa.Column('average_rating', sa.Float(), nullable=True),
    sa.Column('rating_count', sa.Integer(), nullable=True),
    sa.Column('attached_count', sa.Integer(), nullable=True),
    sa.Column('favorite_count', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['link_id'], ['link.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('link_id')
    )
    op.create_table('link_summary_embedding',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('link_id', sa.Integer(), nullable=False),
    sa.Column('summary_content', sa.Text(), nullable=False),
    sa.Column('summary_vector', Vector(dim=1536), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['link_id'], ['link.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('link_id')
    )
    op.create_table('chat_room',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('folder_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('is_favorite', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['folder_id'], ['folder.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['user_id'], ['user_info.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('chat_room_link',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('chat_room_id', sa.Integer(), nullable=True),
    sa.Column('link_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['chat_room_id'], ['chat_room.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['link_id'], ['link.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('chat_room_id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('is_user_message', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['chat_room_id'], ['chat_room.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rating',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('message_id', sa.Integer(), nullable=False),
    sa.Column('score', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['message_id'], ['message.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('message_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rating')
    op.drop_table('message')
    op.drop_table('chat_room_link')
    op.drop_table('chat_room')
    op.drop_table('link_summary_embedding')
    op.drop_table('link_stat')
    op.drop_table('folder')
    op.drop_table('user_info')
    op.drop_table('link')
    # ### end Alembic commands ###
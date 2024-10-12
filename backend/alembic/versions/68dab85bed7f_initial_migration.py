"""initial migration

Revision ID: 68dab85bed7f
Revises: 
Create Date: 2024-10-12 16:15:39.839744

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pgvector


# revision identifiers, used by Alembic.
revision: str = '68dab85bed7f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # user_info 테이블 생성
    op.create_table('user_info',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # folder 테이블 생성
    op.create_table('folder',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user_info.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # chat_room 테이블 생성
    op.create_table('chat_room',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('folder_id', sa.Integer(), nullable=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('is_favorite', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user_info.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['folder_id'], ['folder.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )

    # link 테이블 생성
    op.create_table('link',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('url', sa.String(), nullable=False, unique=True),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # link_stat 테이블 생성
    op.create_table('link_stat',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('link_id', sa.Integer(), nullable=False, unique=True),
        sa.Column('average_rating', sa.Float(), nullable=True),
        sa.Column('rating_count', sa.Integer(), nullable=True),
        sa.Column('attached_count', sa.Integer(), nullable=True),
        sa.Column('favorite_count', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['link_id'], ['link.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # link_summary_embedding 테이블 생성
    op.create_table('link_summary_embedding',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('link_id', sa.Integer(), nullable=False, unique=True),
        sa.Column('summary_content', sa.Text(), nullable=False),
        sa.Column('summary_vector', pgvector.sqlalchemy.Vector(dim=1536), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['link_id'], ['link.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # chat_room_link 테이블 생성
    op.create_table('chat_room_link',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('chat_room_id', sa.Integer(), nullable=True),
        sa.Column('link_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['chat_room_id'], ['chat_room.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['link_id'], ['link.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )

    # message 테이블 생성
    op.create_table('message',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('chat_room_id', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('is_user_message', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['chat_room_id'], ['chat_room.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # rating 테이블 생성
    op.create_table('rating',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('message_id', sa.Integer(), nullable=False, unique=True),
        sa.Column('score', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['message_id'], ['message.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('rating')
    op.drop_table('message')
    op.drop_table('chat_room_link')
    op.drop_table('link_summary_embedding')
    op.drop_table('link_stat')
    op.drop_table('link')
    op.drop_table('chat_room')
    op.drop_table('folder')
    op.drop_table('user_info')

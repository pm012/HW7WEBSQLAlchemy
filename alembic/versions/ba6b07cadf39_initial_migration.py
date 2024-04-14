"""Initial migration

Revision ID: ba6b07cadf39
Revises: 
Create Date: 2024-04-14 20:42:37.030612

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'ba6b07cadf39'
down_revision: str = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'groups',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('group_code', sa.String(length=50), nullable=True),
        sa.Column('group_name', sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'students',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=True),
        sa.Column('group_id', sa.Integer(), sa.ForeignKey('groups.id'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'teachers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('teacher_name', sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'subjects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('subj_name', sa.String(length=100), nullable=True),
        sa.Column('teacher_id', sa.Integer(), sa.ForeignKey('teachers.id'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'grades',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), sa.ForeignKey('students.id'), nullable=True),
        sa.Column('subject_id', sa.Integer(), sa.ForeignKey('subjects.id'), nullable=True),
        sa.Column('grade', sa.Integer(), nullable=True),
        sa.Column('date', sa.Date(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('grades')
    op.drop_table('subjects')
    op.drop_table('teachers')
    op.drop_table('students')
    op.drop_table('groups')

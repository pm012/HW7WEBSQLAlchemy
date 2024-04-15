"""initial migration

Revision ID: 2c67bfa6b665
Revises: 
Create Date: 2024-04-15 18:27:03.184045

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

metadata = sa.MetaData()
# revision identifiers, used by Alembic.
revision: str = '2c67bfa6b665'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    metadata.bind = op.get_bind()
    existing_tables = metadata.tables.keys()
    # Create the 'groups' table
    if 'groups'  not in existing_tables:
        op.create_table(
            'groups',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('group_code', sa.String(length=50), nullable=True),
            sa.Column('group_name', sa.String(length=100), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )

    # Create the 'students' table
    if 'students'  not in existing_tables:
        op.create_table(
            'students',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(length=100), nullable=True),
            sa.Column('group_id', sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
            sa.PrimaryKeyConstraint('id')
        )

    # Create the 'teachers' table
    if 'teachers'  not in existing_tables:
        op.create_table(
            'teachers',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('teacher_name', sa.String(length=100), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )

    # Create the 'subjects' table
    if 'subjects'  not in existing_tables:
        op.create_table(
            'subjects',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('subj_name', sa.String(length=100), nullable=True),
            sa.Column('teacher_id', sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'], ),
            sa.PrimaryKeyConstraint('id')
        )

    # Create the 'grades' table
    if 'grades'  not in existing_tables:
        op.create_table(
            'grades',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('student_id', sa.Integer(), nullable=True),
            sa.Column('subject_id', sa.Integer(), nullable=True),
            sa.Column('grade', sa.Integer(), nullable=True),
            sa.Column('date', sa.Date(), nullable=True),
            sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
            sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], ),
            sa.PrimaryKeyConstraint('id')
        )


def downgrade() -> None:
    metadata.bind = op.get_bind()
    existing_tables = metadata.tables.keys()
    # Drop the 'grades' table
    if 'grades'  not in existing_tables:
        op.drop_table('grades')

    # Drop the 'subjects' table
    if 'subjects'  not in existing_tables:
        op.drop_table('subjects')

    # Drop the 'teachers' table
    if 'teachers'  not in existing_tables:
        op.drop_table('teachers')

    # Drop the 'students' table
    if 'students'  not in existing_tables:
        op.drop_table('students')

    # Drop the 'groups' table
    if 'groups'  not in existing_tables:
        op.drop_table('groups')


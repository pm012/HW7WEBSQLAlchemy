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
    if 'groups' not in existing_tables:
        with op.batch_alter_table('groups') as batch_op:
            batch_op.create_column(sa.Column('id', sa.Integer(), nullable=False))
            batch_op.create_column(sa.Column('group_code', sa.String(length=50), nullable=True))
            batch_op.create_column(sa.Column('group_name', sa.String(length=100), nullable=True))
            batch_op.create_primary_key('pk_groups', ['id'])

    # Create the 'students' table
    if 'students' not in existing_tables:
        with op.batch_alter_table('students') as batch_op:
            batch_op.create_column(sa.Column('id', sa.Integer(), nullable=False))
            batch_op.create_column(sa.Column('name', sa.String(length=100), nullable=True))
            batch_op.create_column(sa.Column('group_id', sa.Integer(), nullable=True))
            batch_op.create_foreign_key('fk_students_group_id_groups', 'groups', ['group_id'], ['id'])
            batch_op.create_primary_key('pk_students', ['id'])

    # Create the 'teachers' table
    if 'teachers' not in existing_tables:
        with op.batch_alter_table('teachers') as batch_op:
            batch_op.create_column(sa.Column('id', sa.Integer(), nullable=False))
            batch_op.create_column(sa.Column('teacher_name', sa.String(length=100), nullable=True))
            batch_op.create_primary_key('pk_teachers', ['id'])

    # Create the 'subjects' table
    if 'subjects' not in existing_tables:
        with op.batch_alter_table('subjects') as batch_op:
            batch_op.create_column(sa.Column('id', sa.Integer(), nullable=False))
            batch_op.create_column(sa.Column('subj_name', sa.String(length=100), nullable=True))
            batch_op.create_column(sa.Column('teacher_id', sa.Integer(), nullable=True))
            batch_op.create_foreign_key('fk_subjects_teacher_id_teachers', 'teachers', ['teacher_id'], ['id'])
            batch_op.create_primary_key('pk_subjects', ['id'])

    # Create the 'grades' table
    if 'grades' not in existing_tables:
        with op.batch_alter_table('grades') as batch_op:
            batch_op.create_column(sa.Column('id', sa.Integer(), nullable=False))
            batch_op.create_column(sa.Column('student_id', sa.Integer(), nullable=True))
            batch_op.create_column(sa.Column('subject_id', sa.Integer(), nullable=True))
            batch_op.create_column(sa.Column('grade', sa.Integer(), nullable=True))
            batch_op.create_column(sa.Column('date', sa.Date(), nullable=True))
            batch_op.create_foreign_key('fk_grades_student_id_students', 'students', ['student_id'], ['id'])
            batch_op.create_foreign_key('fk_grades_subject_id_subjects', 'subjects', ['subject_id'], ['id'])
            batch_op.create_primary_key('pk_grades', ['id'])


def downgrade() -> None:
    metadata.bind = op.get_bind()
    existing_tables = metadata.tables.keys()
    # Drop the 'grades' table
    if 'grades' in existing_tables:
        with op.batch_alter_table('grades') as batch_op:
            batch_op.drop_column('date')
            batch_op.drop_column('grade')
            batch_op.drop_column('subject_id')
            batch_op.drop_column('student_id')
            batch_op.drop_constraint('fk_grades_student_id_students', type_='foreignkey')
            batch_op.drop_constraint('fk_grades_subject_id_subjects', type_='foreignkey')
            batch_op.drop_constraint('pk_grades', type_='primary')

    # Drop the 'subjects' table
    if 'subjects' in existing_tables:
        with op.batch_alter_table('subjects') as batch_op:
            batch_op.drop_constraint('fk_subjects_teacher_id_teachers', type_='foreignkey')
            batch_op.drop_column('teacher_id')
            batch_op.drop_column('subj_name')
            batch_op.drop_constraint('pk_subjects', type_='primary')

    # Drop the 'teachers' table
    if 'teachers' in existing_tables:
        with op.batch_alter_table('teachers') as batch_op:
            batch_op.drop_column('teacher_name')
            batch_op.drop_constraint('pk_teachers', type_='primary')

    # Drop the 'students' table
    if 'students' in existing_tables:
        with op.batch_alter_table('students') as batch_op:
            batch_op.drop_constraint('fk_students_group_id_groups', type_='foreignkey')
            batch_op.drop_column('group_id')
            batch_op.drop_column('name')
            batch_op.drop_constraint('pk_students', type_='primary')

    # Drop the 'groups' table
    if 'groups' in existing_tables:
        with op.batch_alter_table('groups') as batch_op:
            batch_op.drop_column('group_name')
            batch_op.drop_column('group_code')
            batch_op.drop_column('id')
            batch_op.drop_constraint('pk_groups', type_='primary')

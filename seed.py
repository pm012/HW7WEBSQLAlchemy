from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_model import Group, Student, Teacher, Subject, Grade
import random

if __name__ == "__main__":
    # Create SQLAlchemy engine
    engine = create_engine('postgresql://username:password@localhost/dbname')

    # Create a session maker
    Session = sessionmaker(bind=engine)
    session = Session()

    # Seed the database with random data using Faker
    fake = Faker()

    # Create groups
    # TODO add groups and groups codes dictionary
    groups_data = [{'group_code': fake.random_int(100, 999), 'group_name': fake.company()} for _ in range(5)]
    groups = [Group(**data) for data in groups_data]
    session.add_all(groups)
    session.commit()

    # Create teachers
    teachers_data = [{'teacher_name': fake.name()} for _ in range(3)]
    teachers = [Teacher(**data) for data in teachers_data]
    session.add_all(teachers)
    session.commit()

    # Create subjects
    # TODO create list with subject names and pick it from the list
    subjects_data = [{'subj_name': fake.word(), 'teacher_id': random.choice(teachers).id} for _ in range(5)]
    subjects = [Subject(**data) for data in subjects_data]
    session.add_all(subjects)
    session.commit()

    # Create students
    students_data = [{'name': fake.name(), 'group_id': random.choice(groups).id} for _ in range(30)]
    students = [Student(**data) for data in students_data]
    session.add_all(students)
    session.commit()

    # Create grades
    grades_data = [{'student_id': random.choice(students).id, 'subject_id': random.choice(subjects).id,
                    'grade': random.randint(1, 12), 'date': fake.date_this_year()} for _ in range(20)]
    grades = [Grade(**data) for data in grades_data]
    session.add_all(grades)
    session.commit()

    # Close the session
    session.close()

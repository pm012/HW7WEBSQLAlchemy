from faker import Faker
from sqlalchemy.orm import sessionmaker
from db_model import Group, Student, Teacher, Subject, Grade
import random
from engine_gen import EngineManager

if __name__ == "__main__":
    # Group names and subjects        
    groups = {'AM-24-01' : 'Applied Mathematics', 'CS-24-01' : 'Computer Science', 'AI-24-01' : 'Computer Cybernetics and AI'}
    subjects = ['Mathematical Analysis', 'Descrete Mathematics', 'Matematical Modeling', 'Statistics', 'Object Oriented Programming (C++)', 'Voice Recognition', 'Coputer Graphics']
    NUMBER_OF_TEACHERS = 5
    NUMBER_OF_STUDENTS = 30
    GRADE_RANGE = (1, 12)

    
    # Create SQLAlchemy engine
    engine = EngineManager().get_engine()


    # Create a session maker
    Session = sessionmaker(bind=engine)
    session = Session()

    # Seed the database with random data using Faker
    fake = Faker()

    # Create groups        
    groups_data = [{'group_code': key, 'group_name': value} for key, value in groups.items()]
    groups = [Group(**data) for data in groups_data]
    session.add_all(groups)
    session.commit()

    # Create teachers
    teachers_data = [{'teacher_name': fake.name()} for _ in range(NUMBER_OF_TEACHERS)]
    teachers = [Teacher(**data) for data in teachers_data]
    session.add_all(teachers)
    session.commit()

    # Create subjects    
    subjects_data = [{'subj_name': subject_name, 'teacher_id': random.choice(teachers).id} for subject_name in subjects]
    subjects = [Subject(**data) for data in subjects_data]
    session.add_all(subjects)
    session.commit()

    # Create students
    students_data = [{'name': fake.name(), 'group_id': random.choice(groups).id} for _ in range(NUMBER_OF_STUDENTS)]
    students = [Student(**data) for data in students_data]
    session.add_all(students)
    session.commit()

    # Create grades
    grades_data = [{'student_id': random.choice(students).id, 'subject_id': random.choice(subjects).id,
                    'grade': random.randint(GRADE_RANGE[0], GRADE_RANGE[1]), 'date': fake.date_this_year()} for _ in range(20)]
    grades = [Grade(**data) for data in grades_data]
    session.add_all(grades)
    session.commit()

    # Close the session
    session.close()

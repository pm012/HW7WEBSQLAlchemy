from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Mapped, mapped_column
from faker import Faker
import random

# Create SQLAlchemy engine
engine = create_engine('postgresql://username:password@localhost/dbname')

# Create a base class for declarative models
Base = declarative_base()

# Define the SQLAlchemy models
class Group(Base):
    __tablename__ = 'groups'

    id: Mapped[Integer] = mapped_column(primary_key=True)    
    group_code: Mapped[str] = mapped_column(String(50))
    group_name: Mapped[str] = mapped_column(String(50))
    students = relationship('Student', backref='group')


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    group_id = Column(Integer, ForeignKey('groups.id'))
    grades = relationship('Grade', backref='student')


class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True)
    teacher_name = Column(Text)
    subjects = relationship('Subject', backref='teacher')


class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True)
    subj_name = Column(Text)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    grades = relationship('Grade', backref='subject')


class Grade(Base):
    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    grade = Column(Integer)
    date = Column(Date)

if __name__ == "__main__":
    # Create tables in the database
    Base.metadata.create_all(engine)

    # Create a session maker
    Session = sessionmaker(bind=engine)
    session = Session()

    # Seed the database with random data using Faker
    fake = Faker()

    # Create groups
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
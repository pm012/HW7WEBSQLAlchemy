from sqlalchemy import create_engine, Integer, String, ForeignKey, Date
from typing import Optional, List
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Mapped, mapped_column
from engin_gen import EngineManager
from faker import Faker
import random

# Create SQLAlchemy engine
engine = EngineManager()

# Create a base class for declarative models
Base = declarative_base()

# Define the SQLAlchemy models
class Group(Base):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)    
    group_code: Mapped[str] = mapped_column(String(50))
    group_name: Mapped[str] = mapped_column(String(100))
    students = Mapped[List["Student"]] = relationship('Student', backref='group', cascade="all, delete-orphan") 


class Student(Base):
    __tablename__ = 'students'

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    group_id: Mapped[str] = mapped_column(Integer, ForeignKey('groups.id'))
    grades = Mapped[List["Grade"]] = relationship('Grade', backref='student', cascade="all, delete-orphan")


class Teacher(Base):
    __tablename__ = 'teachers'

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True)
    teacher_name: Mapped[str] = mapped_column(String(100))
    subjects = Mapped[List["Subject"]] = relationship('Subject', backref='teacher', cascade="all, delete-orphan")


class Subject(Base):
    __tablename__ = 'subjects'

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True)
    subj_name: Mapped[str] = mapped_column(String(50))
    teacher_id: Mapped[Integer] = mapped_column(Integer, ForeignKey('teachers.id'))
    grades = relationship('Grade', backref='subject')


class Grade(Base):
    __tablename__ = 'grades'

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[Integer] = mapped_column(Integer, ForeignKey('students.id'))
    subject_id: Mapped[Integer] = mapped_column(Integer, ForeignKey('subjects.id'))
    grade: Mapped[Integer] = mapped_column(Integer)
    date: Mapped[Date] = mapped_column(Date)

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

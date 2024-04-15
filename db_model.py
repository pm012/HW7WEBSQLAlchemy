from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Mapped, mapped_column
from sqlalchemy.sql.sqltypes import Date as DateType
from engine_gen import EngineManager

# Create SQLAlchemy engine
engine = EngineManager().get_engine()

# Create a base class for declarative models
Base = declarative_base()

# Define the SQLAlchemy models
class Group(Base):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)    
    group_code: Mapped[str] = mapped_column(String(50))
    group_name: Mapped[str] = mapped_column(String(100))
    students: Mapped[list["Student"]] = relationship(backref='group', cascade="all, delete-orphan")


class Student(Base):
    __tablename__ = 'students'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    group_id: Mapped[str] = mapped_column(Integer, ForeignKey('groups.id'))
    grades: Mapped[list["Grade"]] = relationship(backref='student', cascade="all, delete-orphan")


class Teacher(Base):
    __tablename__ = 'teachers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    teacher_name: Mapped[str] = mapped_column(String(100))
    subjects: Mapped[list["Subject"]] = relationship(backref='teacher', cascade="all, delete-orphan")


class Subject(Base):
    __tablename__ = 'subjects'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    subj_name: Mapped[str] = mapped_column(String(100))
    teacher_id: Mapped[int] = mapped_column(Integer, ForeignKey('teachers.id'))
    grades: Mapped[list["Grade"]] = relationship(backref='subject', cascade="all, delete-orphan")


class Grade(Base):
    __tablename__ = 'grades'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey('students.id'))
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey('subjects.id'))
    grade: Mapped[int] = mapped_column(Integer)
    date: Mapped[DateType] = mapped_column(DateType)

if __name__ == "__main__":
    # Create tables in the database
    Base.metadata.create_all(engine)

    # Create a session maker
    Session = sessionmaker(bind=engine)
    session = Session()   
    session.close()

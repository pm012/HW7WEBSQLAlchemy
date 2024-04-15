from engine_gen import EngineManager
from sqlalchemy.orm import sessionmaker
from db_model import Student, Teacher, Grade, Group, Subject
from sqlalchemy import func

# 1 Find 5 students with the largest average score of all subjects.
def query_1(session):
    res = session.query(Student.name, func.avg(Grade.grade).label('avg_grade')) \
    .join(Grade, Student.id == Grade.student_id) \
    .group_by(Student.id) \
    .order_by(func.avg(Grade.grade).desc()) \
    .limit(5) \
    .all()

    return res

# 2. Find a student with the highest average score from a particular subject.
def query_2(session):
    subject_name = input("Enter the subject name: ")
    res = session.query(Student.name, func.avg(Grade.grade).label('avg_grade')) \
        .join(Grade, Student.id == Grade.student_id) \
        .join(Subject, Grade.subject_id == Subject.id) \
        .filter(Subject.subj_name == subject_name) \
        .group_by(Student.id) \
        .order_by(func.avg(Grade.grade).desc()) \
        .limit(1) \
        .all()
    
    return res

# 3. Find the average score in groups from a particular subject.
def query_3(session):
    subject_name = input("Enter the subject name: ")
    res = session.query(Group.group_name, func.avg(Grade.grade).label('avg_grade')) \
        .join(Student, Group.id == Student.group_id) \
        .join(Grade, Student.id == Grade.student_id) \
        .join(Subject, Grade.subject_id == Subject.id) \
        .filter(Subject.subj_name == subject_name) \
        .group_by(Group.id) \
        .all()
    
    return res

# 4. Find the average score on the stream (all the rating table).
def query_4(session):
    res = session.query(func.avg(Grade.grade)).scalar()
    return res

# 5. Find what courses a certain teacher is reading.
def query_5(session):
    teacher_name = input("Enter the teacher name: ")
    res = session.query(Subject.subj_name) \
        .join(Teacher, Subject.teacher_id == Teacher.id) \
        .filter(Teacher.teacher_name == teacher_name) \
        .group_by(Subject.subj_name) \
        .all()
    
    return res

# 6. Find a list of students in a particular group.
def query_6(session):
    group_name = input("Enter the group name: ")
    res = session.query(Student.name) \
        .join(Group, Student.group_id == Group.id) \
        .filter(Group.group_name == group_name) \
        .all()
    
    return res

# 7. Find students' grades in a separate group from a particular subject.
def query_7(session):
    group_name = input("Enter the group name: ")
    subject_name = input("Enter the subject name: ")
    res = session.query(Student.name, Grade.grade, Grade.date) \
        .join(Group, Student.group_id == Group.id) \
        .join(Grade, Student.id == Grade.student_id) \
        .join(Subject, Grade.subject_id == Subject.id) \
        .filter(Group.group_name == group_name) \
        .filter(Subject.subj_name == subject_name) \
        .all()
    
    return res

# 8. Find the average score that a certain teacher puts in his subjects.
def query_8(session):
    teacher_name = input("Enter the teacher name: ")
    res = session.query(Subject.subj_name, Teacher.teacher_name, func.avg(Grade.grade).label('avg_grade')) \
        .join(Teacher, Subject.teacher_id == Teacher.id) \
        .join(Grade, Subject.id == Grade.subject_id) \
        .filter(Teacher.teacher_name == teacher_name) \
        .group_by(Subject.subj_name) \
        .all()
    
    return res

# 9. Find a list of courses that a particular student attends.
def query_9(session):
    student_name = input("Enter the student name: ")
    res = session.query(Subject.subj_name) \
        .join(Grade, Subject.id == Grade.subject_id) \
        .join(Student, Grade.student_id == Student.id) \
        .join(Group, Student.group_id == Group.id) \
        .filter(Student.name == student_name) \
        .all()
    
    return res

# 10. A list of courses taught to a specific student by a specific teacher.
def query_10(session):
    student_name = input("Enter the student name: ")
    teacher_name = input("Enter the teacher name: ")
    res = session.query(Subject.subj_name) \
        .join(Grade, Subject.id == Grade.subject_id) \
        .join(Student, Grade.student_id == Student.id) \
        .join(Group, Student.group_id == Group.id) \
        .join(Teacher, Subject.teacher_id == Teacher.id) \
        .filter(Student.name == student_name) \
        .filter(Teacher.teacher_name == teacher_name) \
        .all()
    
    return res


def get_handler(num, queries):
    return queries[num]

if __name__ == "__main__":
    queries = {i: globals()[f'query_{i}'] for i in range(1, 11)}
    tasks = {
        1: "Find the 5 students with the highest GPA(grate point average) across all subjects.",
        2: "Find the student with the highest GPA in a particular subject.",
        3: "Find the average score in groups for a certain subject.",
        4: "Find the average score on the stream (across the entire scoreboard grades table).",
        5: "Find what courses a particular teacher teaches.",
        6: "Find a list of students in a specific group.",
        7: "Find the grades of students in a separate group for a specific subject.",
        8: "Find the average score given by a certain teacher in his subjects.",
        9: "Find a list of courses a student is taking.",
        10: "A list of courses taught to a specific student by a specific teacher."

    }



    engine = EngineManager().get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    num = -1
   
    while num != 0:
        try:
            num = int(input(" Please enter number of query 1-10 or 0 to exit: "))
        except  ValueError:
            print("Impossible to get number.")
            continue

        if num in range(1, 11):
            print(f'{tasks[num]}: ')
            print(get_handler(num, queries)(session))
        elif num != 0:
            print("Incorrect number, please enter number from 1 to 10")
            continue

    
    

    
    

    session.close()

   
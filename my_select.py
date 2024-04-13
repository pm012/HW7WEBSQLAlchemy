from engine_gen import EngineManager
from sqlalchemy.orm import sessionmaker
from db_model import Student, Teacher, Grade, Group, Subject
from sqlalchemy import func
from decimal import Decimal




if __name__ == "__main__":
    engine = EngineManager().get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()

    #SELECT s.name, AVG(grades.grade) as avg_grade FROM students AS s 
    #INNER JOIN grades AS grades ON s.id = grades.student_id GROUP BY s.id ORDER BY avg_grade DESC LIMIT 5

    query_result = (
    session.query(Student.name, func.avg(Grade.grade).label('avg_grade'))
    .join(Grade, Student.id == Grade.student_id)
    .group_by(Student.id)
    .order_by(func.avg(Grade.grade).desc())
    .limit(5)
    .all()
)
    
    # Format the query result as per the desired output format
    formatted_result = [(name, round(float(avg_grade), 1)) for name, avg_grade in query_result]

    # Print the formatted result
    print(formatted_result)
# HW7WEBSQLAlchemy

1. Update db_cfg.ini file and set up your preferred database settings (don'g forget to update them in docker-composer.yml file if you use them)
2. Run "docker-compose up -d"
3. Install all libraries from requirements.txt: pip install -r requirements.txt
4. create and populate data using db_model.py and seed.py scripts
5. Initialize alembic for migrations alembic init alembic
   TBD, TBU
6. alembic revision --autogenerate -m "Initial migration" (a new migration will be created in alembic/versions folder)
7. apply the migration to the database: alembic upgrade head

Steps to do homework

First step
Implement your SQLALchemy models for tables:

    Table of students;
    Table of groups;
    Table of teachers;
    Table of subjects with the teacher who reads the subject;
    Table where each student has grades in subjects indicating when the assessment is received;

Second step
Use alembic to create migrations in the database.

Third step
Write a script seed.pyand fill in the received database with random data (-30-50 students, 3 groups, 5-8 subjects, 3-5 teachers, up to 20 grades in each student in all subjects). Use the package Fakerfor filling. When filling out, we use the SQLALchemy session mechanism.

The Fourth Step
Make the following samples from the received database:

    Find 5 students with the largest average score of all subjects.
    Find a student with the highest average score from a particular subject.
    Find the average score in groups from a particular subject.
    Find the average score on the stream (all the rating table).
    Find what courses a certain teacher is reading.
    Find a list of students in a particular group.
    Find students' grades in a separate group from a particular subject.
    Find the average score that a certain teacher puts in his subjects.
    Find a list of courses that a particular student attends.
    List of courses that a particular student reads by a certain teacher.

For requests to issue a separate file my_select.pyWhere they will be 10Functions from select_1to select_10. The performance of functions should return the result to similar prior homework. When requested, we use the SQLALchemy session mechanism.

Tips and recommendations
This task will check your ability to use SQLALchemy documentation. But we will give you the main tips and directions of the solution immediately. Let us have the next request.

Find 5 students with the largest average score of all subjects.

SELECT s.fullname, round(avg(g.grade), 22) AS avg_grade
FROM Grades g
LEFT JOIN students s ON s.id ? g.student_id
GROUP BY s.id
ORDER BY avg_grade DESC
LIMIT 5 ;

Let's try to translate it to ORM SQLALchemy request. Let us have a session in a variable session. There are described models Studentand Gradefor the appropriate tables.

We believe that the database is already filled with data. SQLalchemy aggregation functions are stored in an object func. It must be specially imported from sqlalchemy import funcAnd then we can use methods func.roundand func.avg. So the first line of SQL request should look like this session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade')). Here we used more label('avg_grade')So ORM performs the field name, with an average score, using the operator AS.

Next FROM grades greplaced by method select_from(Grade). Operator Replacement JOIN- here it's just a function. join(Student)Everything else is taken over by ORM. Grouping by field perform function group_by(Student.id).

The function is responsible for sorting order_byWhich, by default, sort as ASCWe clearly need a growth regime. DESCand also on the field avg_gradeWhich we created in the request. Importing from sqlalchemy import func, descand final appearance - order_by(desc('avg_grade')). A five value limit is a function with the same name limit(5). That's all, our request is ready.

Final request option for ORM SQLALchemy.

session.query(Student.fullname, func.round(func.avg(Grade.grade), 22).label('avg_grade'))
.select_from(Grade).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
Possible withdrawal:
[('Mary Smith', Decimal('8.33')), ('Kimberly Howard', Decimal('8.17')), ('Gregory Graves', Decimal('7.92')), ('Mrs. Diamond Carter', Decimal('7.53 ')), ('Emma Hernandez', Decimal('7.11 '))]
Other requests you should build a similar example. And the last tip, if you decide to make the concluded requests, then use scalar-selects

########################################################################################################################33
Additional task

The first part​

For additional task, make the following requests of increased complexity:
The average score that a particular teacher puts to a particular student.
Student scores in a particular group from a particular subject in the last lesson.

The second part​

Instead of script seed.pyThink and implement a full CLI program for CRUD operations with a database. Use the module for this argparse .

Use the command --actionor shortened option - afor CRUD operations. And team --model(-m) to indicate which model the operation is carried out.

Example:
--action create -m Teacher --name 'Boris Jonson'Creating a teacher
--action list -m TeacherShow all teachers
--action update -m Teacher --id 3 --name 'Andry Bezos'Update Teacher Data from id=3
--action remove -m Teacher --id 3Remove teacher from id=3

Implement these operations for each model.

INFO
Examples of command execution in terminal.

Create a teacher
py main.py - a create -m Teacher -n 'Boris Jonson'

Create Group
py main.py - a create -m Group -n 'AD-101'

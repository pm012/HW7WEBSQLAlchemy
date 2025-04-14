SQLAlchemy task descirption

1. Update db_cfg.ini file and set up your preferred database settings (don'g forget to update them in docker-composer.yml file if you use them)

2. Run

```bash
   docker-compose up -d
```

3. Install all libraries from requirements.txt:

```bash
pip install -r requirements.txt
```

4. Initialize alembic for migrations:

```bash
alembic init alembic
```

5. Update connection string in alembic.ini file
   (parameter sqlalchemy.url should have postgresql://<username>:<password>@localhost/<databasename>)

6. In env py import db_model module and initialize target_metadata = db_model.Base.metadata

7. Create new migration: alembic revision --autogenerate -m "init" (a new migration will be created in alembic/versions folder). If file in /versions/<id>\_init.py has upgrade() and downgrade() methods without implementation it is required to fill them manually.
   For example, for groups table:

   ```python
   def upgrade() -> None:
    op.create_table(
        'groups',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('group_code', sa.String(length=50), nullable=True),
        sa.Column('group_name', sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint('id')
        ......
        <...other tables initialization...>
        )
    ##################################################



    def downgrade() -> None:
        op.drop_table('grades')
        #drop_table for other tables########

   ```

8. Apply the migration to the database:

```bash
alembic upgrade head
```

9. Create and populate data using db_model.py and seed.py scripts

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
Write a script seed.py and fill in the received database with random data (-30-50 students, 3 groups, 5-8 subjects, 3-5 teachers, up to 20 grades in each student in all subjects). Use the package Fakerfor filling. When filling out, we use the SQLALchemy session mechanism.

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

For requests to issue a separate file my_select.py, There will be 10 functions from select_1 to select_10. The functions should return the result similar to prior homework. It should be used the SQLALchemy session mechanism.

Tips and recommendations
This task will check your ability to use SQLALchemy documentation. But we will give you the main tips and directions of the solution immediately. Let us have the next request.

Find 5 students with the largest average score of all subjects.

```SQL
SELECT s.fullname, round(avg(g.grade), 22) AS avg_grade
FROM Grades g
LEFT JOIN students s ON s.id ? g.student_id
GROUP BY s.id
ORDER BY avg_grade DESC
LIMIT 5 ;
```

Let's try to translate it to ORM SQLALchemy request. Let us have a session in a variable session. There are described models Studentand Gradefor the appropriate tables.

We believe that the database is already filled with data. SQLalchemy aggregation functions are stored in an object func. It must be specially imported from sqlalchemy import funcAnd then we can use methods func.roundand func.avg. So the first line of SQL request should look like this session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade')). Here we used more label('avg_grade')So ORM performs the field name, with an average score, using the operator AS.

Next FROM grades greplaced by method select_from(Grade). Operator Replacement JOIN- here it's just a function. join(Student)Everything else is taken over by ORM. Grouping by field perform function group_by(Student.id).

The function is responsible for sorting order_byWhich, by default, sort as ASCWe clearly need a growth regime. DESCand also on the field avg_gradeWhich we created in the request. Importing from sqlalchemy import func, descand final appearance - order_by(desc('avg_grade')). A five value limit is a function with the same name limit(5). That's all, our request is ready.

Final request option for ORM SQLALchemy.

```python
session.query(Student.fullname, func.round(func.avg(Grade.grade), 22).label('avg_grade')).select_from(Grade).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
```

Possible output:

```bash
[('Mary Smith', Decimal('8.33')), ('Kimberly Howard', Decimal('8.17')), ('Gregory Graves', Decimal('7.92')), ('Mrs. Diamond Carter', Decimal('7.53 ')), ('Emma Hernandez', Decimal('7.11 '))]
```

Other requests you should build a similar example. And the last tip, if you decide to make the concluded requests, then use scalar-selects

########################################################################################################################

Additional task (not implemented)

The first part​

For additional task, make the following requests of increased complexity:
The average score that a particular teacher puts to a particular student.
Student scores in a particular group from a particular subject in the last lesson.

The second part​

Instead of script seed.pyThink and implement a full CLI program for CRUD operations with a database. Use the module for this <b>argparse</b> .

Use the command --action or shortened option -a and for CRUD operations. And team --model(-m) to indicate which model the operation is carried out.

Example:

```bash
--action create -m Teacher --name 'Boris Jonson'Creating a teacher
--action list -m TeacherShow all teachers
--action update -m Teacher --id 3 --name 'Andry Bezos'Update Teacher Data from id=3
--action remove -m Teacher --id 3Remove teacher from id=3
```

Implement these operations for each model.

INFO
Examples of command execution in terminal.

Create a teacher

```bash
py main.py - a create -m Teacher -n 'Boris Jonson'
```

Create Group

```bash
py main.py - a create -m Group -n 'AD-101'
```

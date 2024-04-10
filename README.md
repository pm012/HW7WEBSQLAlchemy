# HW7WEBSQLAlchemy
1. Update db_cfg.ini file and set up your preferred database settings (don'g forget to update them in docker-composer.yml file if you use them)
2. Run "docker-compose run" TBD
3. Install all libraries from requirements.txt: pip install -r requirements.txt
5. create and populate data using db_model.py and seed.py scripts
4. Initialize alembic for migrations alembic init alembic
TBD, TBU
5. alembic revision --autogenerate -m "Initial migration" (a new migration will be created in alembic/versions folder)
6. apply the migration to the database: alembic upgrade head



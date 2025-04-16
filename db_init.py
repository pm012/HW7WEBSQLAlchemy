# Init the session
from engine_gen import EngineManager
from sqlalchemy.orm import sessionmaker

engine = EngineManager().get_engine()
Session = sessionmaker(bind=engine)
session = Session()

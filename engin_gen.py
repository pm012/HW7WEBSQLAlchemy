from sqlalchemy import create_engine
import configparser
CONFIG_FILE = "db_cfg.ini"

class EngineManager:
    def __init__(self, db_type="postgres"):        
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        username = config.get('postgres', 'username') 
        password = config.get('postgres', 'password') 
        host = config.get('postgres', 'username') 
        port = config.get('postgres', 'port')
        db_name = config.get('postgres', 'db_name') 
        self.db_url = f'postgresql://{username}:{password}@{host}:{port}/{db_name}'

    def get_engine(self):
        
        engine = create_engine(self.db_url)

from sqlalchemy import create_engine
import configparser

CONFIG_FILE = "db_cfg.ini"

class EngineManager:
    _shared_state = {}

    def __init__(self, db_type="postgres"):
        self.__dict__ = self._shared_state

        if not hasattr(self, "initialized"):  # Prevent re-init
            self.initialized = True
            self.engine = None
            config = configparser.ConfigParser()
            config.read(CONFIG_FILE)

            if db_type == 'postgres':
                username = config.get('postgres', 'username')
                password = config.get('postgres', 'password')
                host = config.get('postgres', 'host')
                port = config.get('postgres', 'port')
                db_name = config.get('postgres', 'db_name')
                self.db_url = f'postgresql://{username}:{password}@{host}:{port}/{db_name}'
            else:
                raise ValueError(f"The type of database '{db_type}' is not implemented")

            print('EngineManager initialized')

    def get_engine(self):
        if self.engine is None:
            self.engine = create_engine(self.db_url)
            print("Created engine for:", self.db_url)
        else:
            print("Using existing engine")
        return self.engine

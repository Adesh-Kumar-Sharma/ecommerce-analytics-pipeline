import os
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://username:password@hostname:port/database')

class DatabaseManager:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.metadata = MetaData()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def get_connection(self):
        return self.engine.connect()
    
    def execute_query(self, query, params=None):
        with self.get_connection() as conn:
            if params:
                return pd.read_sql(query, conn, params=params)
            return pd.read_sql(query, conn)
    
    def insert_dataframe(self, df, table_name, if_exists='append'):
        df.to_sql(table_name, self.engine, if_exists=if_exists, index=False)
    
    def execute_sql_file(self, file_path):
        with self.engine.begin() as conn:
            with open(file_path, 'r') as file:
                sql_commands = file.read().split(';')
                for command in sql_commands:
                    if command.strip():
                        conn.execute(text(command))

# Initialize database manager
db_manager = DatabaseManager()

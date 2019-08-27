from psycopg2 import connect, DatabaseError, OperationalError
from psycopg2.errors import DuplicateDatabase
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime, date, time, timezone

class Database:

    def __init__(self):
        self.conn_conf = None
        self.connection = None
        self.cursor = None

    def configure_connection(self, user, password, host="localhost", database=""):
        if database == "":
            self.conn_conf = {
                "user": user,
                "password": password,
                "host": host
            }
        else: 
            self.conn_conf = {
                "user": user,
                "password": password,
                "host": host,
                "database": database
            }

    def create_database(self, name):
        if self.connection != None:
            try:
                self.connection.cursor().execute(f"CREATE DATABASE {name};")
            except DuplicateDatabase as e:
                print(e)
    
    def reconnect(self):
        if self.conn_conf != None and self.connection != None:
            self.connection.close()
            self.connection = connect(**self.conn_conf)
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        else:
            raise OperationalError("Connection configuration is not set!")
    
    def connect(self):
        if self.conn_conf == None:
            raise OperationalError("Connection configuration is not set!")
        else:
            self.connection = connect(**self.conn_conf)
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    def disconnect(self):
        if self.connection != None:
            self.connection.close()
        else:
            try:
                raise OperationalError("There is no connection live!")
            except OperationalError as e:
                print(e)
    
    def enable_cursor(self):
        if self.connection != None:
            self.cursor = self.connection.cursor()
        else:
            raise OperationalError("No database connected!")

    def retrieve_table_info(self, table_name):
        if self.cursor != None:
            #print(f"Select * FROM {table_name};")
            self.cursor.execute(f"Select * FROM  {table_name};")
            colnames = [(desc[0],desc[1]) for desc in self.cursor.description]
            return colnames
        else:
            raise OperationalError("No live connection to any database")

    def retrieve_table_records(self, table_name):
        if self.cursor != None:
            #print(f"Select * FROM {table_name};")
            self.cursor.execute(f"Select * FROM {table_name};")
            return [i for i in self.cursor]
        else:
            raise OperationalError("No live connection to any database")     
import os
import sqlite3
from contextlib import contextmanager

DB_PATH = os.path.join("data", "baza.db")

class Database:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

    def get_connection(self):
        """ Vraća konekciju prema bazi """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def execute_query(self, query, params=()):
        """ INSERT, UPDATE, DELETE upiti """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Greška u execute_query: {e}")
            return None
    
    def fetch_one(self, query, params=()):
        """ Dohvaća jedan red """
        try:

            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                result = cursor.fetchone()
                # rezultat koji je sqlite3.Row se pretvara u dictionary
                return dict(result) if result else None
        except sqlite3.Error as e:
            print(f"Greška u fetch_one: {e}")
            return None
    
    def fetch_all(self, query, params=()):
        """ Dohvaća više redova """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                results = cursor.fetchall()
                return [dict(row) for row in results]
        except sqlite3.Error as e:
            print(f"Greška u fetch_all: {e}")
            return None

    def init_db(self, schema_path="data/schema.sql"):
        """ Čita schemu i stvara tablice ako ne postoje"""
        if not os.path.exists(schema_path):
            print("Schema baze ne postoji")
            return
        
        with open(schema_path, 'r') as f:
            schema_sql = f.read()

        with self.get_connection() as conn:
            conn.executescript(schema_sql)
            print("Inicijalizirana baza prema schemi")

db = Database()
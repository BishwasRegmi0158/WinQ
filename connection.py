import sqlite3 as sql

def get_connection():
  connection = sql.connect('user_database.db')
  return connection
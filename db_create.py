#db_create.py

import sqlite3
from config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as connection:
    #get a cursor objuect used to execute SQL commands
    c = connection.cursor()
    
    #create the table
    c.execute("""CREATE TABLE ftasks(task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, due_date TEXT NOT NULL, priority INTEGER NOT NULL,
        status INTEGER NOT NULL)""")
        
    #insert dummy data into the table
    c.execute('INSERT INTO ftasks (name, due_date, priority, status) VALUES ("Finish this tutorial", "08/13/2013",10,1)')
    c.execute('INSERT INTO ftasks (name, due_date, priority, status) VALUES ("Finish my book", "08/13/2013",10,1)')
    
    
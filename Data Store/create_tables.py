import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE sleep
          (id INTEGER PRIMARY KEY ASC, 
           user_id VARCHAR(250) NOT NULL,
           sleep_start_time VARCHAR(250) NOT NULL,
           sleep_end_time VARCHAR(250) NOT NULL,
           feeling VARCHAR(250) NOT NULL,
           notes VARCHAR(250) NOT NULL,
           date_created VARCHAR(250) NOT NULL)
          ''')

c.execute('''
          CREATE TABLE day
          (id INTEGER PRIMARY KEY ASC, 
           user_id VARCHAR(250) NOT NULL,
           mood VARCHAR(250) NOT NULL,
           notes VARCHAR(250) NOT NULL,
           date_created VARCHAR(250) NOT NULL)
          ''')

conn.commit()
conn.close()

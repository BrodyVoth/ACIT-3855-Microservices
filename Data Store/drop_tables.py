import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute('''
          DROP TABLE sleep;
          ''')
c.execute('''
          DROP TABLE day;
          ''')
conn.commit()
conn.close()

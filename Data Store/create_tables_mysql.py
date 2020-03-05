import mysql.connector

db_conn = mysql.connector.connect(host="localhost", user="root", password="password", database="events")

db_cursor = db_conn.cursor()

db_cursor.execute('''
          CREATE TABLE sleep
          (id INT NOT NULL AUTO_INCREMENT, 
           user_id VARCHAR(250) NOT NULL,
           sleep_start_time VARCHAR(250) NOT NULL,
           sleep_end_time VARCHAR(250) NOT NULL,
           feeling VARCHAR(250) NOT NULL,
           notes VARCHAR(250) NOT NULL,
           date_created VARCHAR(250) NOT NULL,
           CONSTRAINT sleep_pk PRIMARY KEY (id))
          ''')

db_cursor.execute('''
          CREATE TABLE day
          (id INT AUTO_INCREMENT, 
           user_id VARCHAR(250) NOT NULL,
           mood VARCHAR(250) NOT NULL,
           notes VARCHAR(250) NOT NULL,
           date_created VARCHAR(250) NOT NULL,
           CONSTRAINT day_pk PRIMARY KEY (id))
          ''')

db_conn.commit()
db_conn.close()

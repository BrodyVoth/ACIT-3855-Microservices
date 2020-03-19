import mysql.connector

db_conn = mysql.connector.connect(host="ec2-34-220-130-154.us-west-2.compute.amazonaws.com", user="root", password="password", database="events")

db_cursor = db_conn.cursor()

db_cursor.execute('''
          DROP TABLE sleep, day
          ''')

db_conn.commit()
db_conn.close()

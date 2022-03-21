#!/usr/bin/env python

#-----------------------------------------------------------------------
# print_db.py
# Authors:
#-----------------------------------------------------------------------
import psycopg2
#-----------------------------------------------------------------------

# connection establishment
conn = psycopg2.connect(
    database="postgres",
    user='postgres',
    password='postpass1234',
    host='localhost',
    port='5432')


conn.autocommit = True

# Creating a cursor object
cursor = conn.cursor()
cursor.execute(mealx)
print(cursor.fetchall())

# Closing the connection
conn.close()

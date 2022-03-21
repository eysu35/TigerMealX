#!/usr/bin/env python

#-----------------------------------------------------------------------
# create_db.py
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
name_Database = "MealX"

# query to create a database

sql = ''' CREATE database ''' + name_Database

# executing above query
cursor.execute(sql)
print("Database has been created successfully !!");

# Closing the connection
conn.close()



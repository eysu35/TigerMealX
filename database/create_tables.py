#!/usr/bin/env python

#-----------------------------------------------------------------------
# create_tables.py
# Authors:
#-----------------------------------------------------------------------
import psycopg2
#-----------------------------------------------------------------------

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE students (
            PUID SERIAL PRIMARY KEY,
            student_name VARCHAR(255) NOT NULL,
            meal_plan VARCHAR(255) NOT NULL,
            location_ID  SERIAL NOT NULL
        )
        """,
        """ CREATE TABLE locations (
                location_id SERIAL PRIMARY KEY,
                location_name VARCHAR(255) NOT NULL
                )
        """,
        """
        CREATE TABLE friends (
                PUID SERIAL NOT NULL,
                friend_PUID SERIAL NOT NULL,
                PRIMARY KEY (PUID, friend_PUID)
        )
        """,
        """
        CREATE TABLE exchanges (
                mealx_id SERIAL PRIMARY KEY,
                stdnt1_PUID SERIAL NOT NULL,
                stdnt2_PUID SERIAL NOT NULL,
                meal VARCHAR(255) NOT NULL,
                exchge1_date VARCHAR(255),
                exchge1_loc VARCHAR(255),
                exchge2_date VARCHAR(255),
                exchge2_loc VARCHAR(255),
                exp_date VARCHAR(255) NOT NULL,
                status VARCHAR(255) NOT NULL
        )
        """)

    try:
        # connection establishment
        conn = psycopg2.connect(
            database="mealx",
            user='postgres',
            password='postpass1234',
            host='localhost',
            port='5432')

        conn.autocommit = True
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("success")


if __name__ == '__main__':
    create_tables()

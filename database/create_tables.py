#!/usr/bin/env python

#-----------------------------------------------------------------------
# create_tables.py
# Authors:
#-----------------------------------------------------------------------
import psycopg2
from config import config
#-----------------------------------------------------------------------

def create_tables():

    """ create tables in the PostgreSQL database"""
    
    commands = (
        """ DROP TABLE IF EXISTS students, 
                student_plans, friends, 
                locations, exchanges
        """,
        """CREATE EXTENSION IF NOT EXISTS "uuid-ossp"
        """,
        """
        CREATE TABLE students (
            PUID VARCHAR(255) PRIMARY KEY,
            netID VARCHAR(255) NOT NULL,
            student_name VARCHAR(255) NOT NULL,
            meal_plan_id VARCHAR(255) NOT NULL,
            isValidForMealExchange BOOLEAN NOT NULL
        )
        """,
        """ CREATE TABLE student_plans (
                meal_plan_id VARCHAR(255) PRIMARY KEY,
                location_id VARCHAR(255) NOT NULL
                )
        """,
        """
        CREATE TABLE friends (
                PUID VARCHAR(255) NOT NULL,
                friend_PUID VARCHAR(255) NOT NULL,
                PRIMARY KEY (PUID, friend_PUID)
        )
        """,
        """
        CREATE TABLE locations (
                location_id VARCHAR(255) PRIMARY KEY,
                location_name VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE exchanges (
                meal_exchange_id UUID DEFAULT uuid_generate_v4 () 
                PRIMARY KEY,
                student1_PUID VARCHAR(255) NOT NULL,
                student2_PUID VARCHAR(255) NOT NULL,
                meal VARCHAR(255) NOT NULL,
                exchange1_date DATE,
                exchange1_location_id VARCHAR(255),
                exchange2_date DATE,
                exchange2_location_id VARCHAR(255),
                expiration_date DATE NOT NULL,
                status VARCHAR(255) NOT NULL
        )
        """
        )

    conn = None
    try:
        # connection establishment
        params = config()
        conn = psycopg2.connect(**params)
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

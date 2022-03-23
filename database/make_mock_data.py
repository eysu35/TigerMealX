#!/usr/bin/env python

#-----------------------------------------------------------------------
# make_mock_data.py
# Authors:
#-----------------------------------------------------------------------
import psycopg2
from config import config
#-----------------------------------------------------------------------

def add_data(table, row_data):

    if table == 'students':
        sql = '''INSERT INTO students(PUID, student_name, meal_plan,
        location_ID) VALUES (%s, %s, %s, %s)'''

    if table == "locations":
        sql = '''INSERT INTO locations(location_ID,
                location_name) VALUES (%s, %s)'''

    if table == "friends":
        sql = '''INSERT INTO friends(PUID, friend_PUID) VALUES (%s, %s)'''

    if table == "exchanges":
        sql = '''INSERT INTO exchanges(mealx_id, stdnt1_PUID, stdnt2_PUID,
        meal,exchge1_date, exchge1_loc, exchge2_date, exchge2_loc, 
        exp_date, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

    try:
        # connection establishment
        params = config()
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor()

        # add in each row of mock data into the relevant table
        cur.execute(sql, row_data)
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
    # students table
    add_data('students', [920228342, "Ellen Su", "Tiger Inn", 1234])
    add_data('students', [920195317, "Arin Mukherjee", "Dining Hall "
                                                       "Plan", 5678])
    add_data('students', [920227978, "Charles Coppieters", "Cottage",
                          6789])
    add_data('students', [123456789, "Shayna Maleson", "Quad", 4444])
    add_data('students', [112345678, "Floyd Benedikter", "Ivy", 0000])


    # locations table
    add_data('locations', [1234, "Tiger Inn"])
    add_data('locations', [5678, "Dining Hall"])
    add_data('locations', [6789, "Cottage"])
    add_data('locations', [4444, "Quad"])
    add_data('locations', [0000, "Ivy"])

    # friends table
    add_data('friends', [920228342, 123456789])
    add_data('friends', [112345678, 123456789])
    add_data('friends', [920195317, 920228342])
    add_data('friends', [920195317, 112345678])
    add_data('friends', [123456789, 920195317])

    # exchanges table
    add_data('exchanges', [1, 123456789, 112345678, "lunch",
                           "01/01/01", "Ivy", None , None, "04/01/01",
             "Incomplete"])
    add_data('exchanges', [2, 920228341, 920195317, "breakfast",
                           "02/10/15", "Tiger Inn", "03/14/15" ,
                           "Dining Hall",
                           "05/10/15",
             "Complete"])






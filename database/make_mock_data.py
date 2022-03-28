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
        sql = '''INSERT INTO students(puid, netid, student_name, 
        meal_plan_id, isvalidformealexchange) VALUES (%s, %s, %s, %s, %s
        )'''

    if table == 'student_plans':
        sql = '''INSERT INTO student_plans(meal_plan_id, location_id) 
        VALUES (%s, %s)'''

    if table == "locations":
        sql = '''INSERT INTO locations(location_id,
                location_name) VALUES (%s, %s)'''

    if table == "friends":
        sql = '''INSERT INTO friends(puid, friend_puid) VALUES (%s, 
        %s)'''

    if table == "exchanges":
        sql = '''INSERT INTO exchanges(student1_puid, 
        student2_puid, meal, exchange1_date, exchange1_location_id, 
        exchange2_date, exchange2_location_id, expiration_date, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''

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
    add_data('students', ["920228342", "eysu", "Ellen Su", "1111",
                          True])
    add_data('students', ["920195317", "arinm", "Arin Mukherjee",
                          "2222", True])
    add_data('students', ["920227978", "cwallant", "Charles "
                          "Coppieters", "3333", True])
    add_data('students', ["123456789", "smaleson", "Shayna Maleson",
                          "4444", True])
    add_data('students', ["112345678", "floydb", "Floyd Benedikter",
                          "5555", True])
    # add student that does not have valid plan
    add_data('students', ["000000000", "test", "Test Test", "6666",
                          False])
    # add second campus dining student
    add_data('students', ["000000001", "test2", "Test2 Test2", "7777",
                          True])

    # student plans table
    add_data('student_plans', ["1111", "1234"])
    add_data('student_plans', ["2222", "5678"])
    add_data('student_plans', ["3333", "6789"])
    add_data('student_plans', ["4444", "4440"])
    add_data('student_plans', ["5555", "0000"])
    add_data('student_plans', ["6666", "0001"])
    add_data('student_plans', ["7777", "5678"])

    # locations table
    add_data('locations', ["1234", "Tiger Inn"])
    add_data('locations', ["5678", "Campus Dining"])
    add_data('locations', ["6789", "Cottage"])
    add_data('locations', ["4440", "Quad"])
    add_data('locations', ["0000", "Ivy"])
    add_data('locations', ["0001", "Independent"])


    # friends table
    add_data('friends', ["920228342", "123456789"])
    add_data('friends', ["112345678", "123456789"])
    add_data('friends', ["920195317", "920228342"])
    add_data('friends', ["920195317", "112345678"])
    add_data('friends', ["123456789", "920195317"])
    add_data('friends', ["000000000", "920228342"])
    add_data('friends', ["000000001", "920195317"])
    add_data('friends', ["000000001", "123456789"])


    # exchanges table
    add_data('exchanges', ["123456789", "112345678", "lunch",
                           '2001-01-01', 'Ivy', None , None,
                           '2001-01-31', 'Incomplete'])
    add_data('exchanges', ["920228342", "920195317", "breakfast",
                           '2015-02-15', "Tiger Inn", '2015-02-25' ,
                           "Dining Hall", '2015-03-15', "Complete"])
    add_data('exchanges', ["123456789", "920228342", "lunch",
                           None, None, None, None, '2022-04-05',
                           "Incomplete"])






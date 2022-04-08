#!/usr/bin/env python

#-----------------------------------------------------------------------
# make_mock_data.py
# Authors:
#-----------------------------------------------------------------------
import psycopg2
from config import config
import csv
import pandas as pd
import numpy as np
import random
import time
from psycopg2.extensions import register_adapter, AsIs
import uuid
#-----------------------------------------------------------------------

def remove_all_data():
    commands = (
        """ DELETE FROM students
        """,
        """ DELETE FROM student_plans
        """,
        """ DELETE FROM locations
        """,
        """ DELETE FROM friends
        """,
        """ DELETE FROM exchanges
        """,)

    try:
        # connection establishment
        params = config()
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor()

        # add in each row of mock data into the relevant table
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
            # print("success")        

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
            # print("success")
    

def str_time_prop(start, end, time_format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%m/%d/%Y %I:%M %p', prop)

def getRandomDate():
    return random_date("1/1/2021 1:30 PM", "1/1/2022 4:50 AM", random.random())
    # return "hello"

def getRandomMeal():
    meals = ['breakfast','lunch','dinner']
    return meals[np.random.randint(len(meals))]

def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)
def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)

def get_club_from_id(df, puid):
    user = df.loc[df["PUID (number on your prox)"] == puid]
    return user['Meal Plan'].iloc[0]

def location_id_from_location(loc):
    words = loc.lower().split()

    loc_id = "~"
    for word in words:
        loc_id += word + '_'
    loc_id += 'location_id~'

    return loc_id

def main():

    # Takes care of (can't adapt type 'numpy.int64') error
    register_adapter(np.float64, addapt_numpy_float64)
    register_adapter(np.int64, addapt_numpy_int64)

    # Delete data in all ables 
    remove_all_data()
                    
    

    # Locations Table Dictionary
    locations_dict = {'~dining_hall_location_id~': 'Dining Hall',
                            '~terrace_location_id~': 'Terrace', 
                             '~tower_location_id~': 'Tower',
                             '~cannon_location_id~': 'Cannon',
                             '~quad_location_id~': 'Quad',
                             '~colonial_location_id~': 'Colonial',
                             '~ivy_location_id~': 'Ivy',
                             '~ti_location_id~': 'TI',
                             '~cottage_location_id~': 'Cottage',
                             '~cap_location_id~': 'Cap',
                             '~cloister_location_id~': 'Cloister',
                             '~charter_location_id~': 'Charter'}

    # Read csv file as dataframe
    filename = 'Meal Plan Info Form (Responses) - Form Responses 1.csv'
    df = pd.read_csv(filename)

    # Add students/student_plans
    for index, row in df.iterrows():

        rand_id = str(uuid.uuid4())

        # Add student entry
        add_data('students', [row['PUID (number on your prox)'], 
                                row['NetID'], 
                                row['Name'], 
                                rand_id, 
                                True])

        # Add student_plans entry
        add_data('student_plans', [rand_id, location_id_from_location(row['Meal Plan'])])

    
    # Add friends: 
    # Note: Sometimes the same pair is randomly selected multiple times. 
    # However, there is only ever one copy in the table.
    num_friendships = 50
    puids = df.loc[:,"PUID (number on your prox)"]
    for i in range(num_friendships):
        # Get random index
        n1 = np.random.randint(num_friendships)
        
        # Get different random index
        n2 = n1
        while (n1 == n2):
            n2 = np.random.randint(num_friendships)

        # Create friendship from PUIDs of two indices
        add_data('friends', [puids[n1], puids[n2]])

    # Add locations
    for key in locations_dict:
        add_data('locations', [key, locations_dict[key]])
        
    # Add exchanges
    num_exchanges = 50

    # Returns club corresponding to puid
    def getClubFromID(puid):
        user = df.loc[df["PUID (number on your prox)"] == puid]
        return user['Meal Plan'].iloc[0]

    for i in range(num_exchanges):
        # Get random index
        n1 = np.random.randint(num_exchanges)
        
        # Get different random index
        n2 = n1
        while (n1 == n2):
            n2 = np.random.randint(num_exchanges)   

        exchange_params = [puids[n1], puids[n2], getRandomMeal(), getRandomDate(), 
                            getClubFromID(puids[n1]), None, None, getRandomDate(), 'Incomplete']

        add_data('exchanges', exchange_params)


# def add_ellen_and_shayna_exchanges():
#
#     exchange_params = ['920228016', '920228342', getRandomMeal(), getRandomDate(),
#                        'Quad', None, None, getRandomDate(), 'Incomplete']
#     add_data('exchanges', exchange_params)
#
#     exchange_params = ['920228016', '920228342', getRandomMeal(), getRandomDate(),
#                        'TI', None, None, getRandomDate(), 'Incomplete']
#     add_data('exchanges', exchange_params)
#
#     exchange_params = ['920228016', '920228342', getRandomMeal(), getRandomDate(),
#                        'Quad', None, None, getRandomDate(), 'Incomplete']
#     add_data('exchanges', exchange_params)
#
#     exchange_params = ['920228016', '920228342', getRandomMeal(), getRandomDate(),
#                        'TI', None, None, getRandomDate(), 'Incomplete']
#     add_data('exchanges', exchange_params)
#
#     exchange_params = ['920228342', '920228016', getRandomMeal(), getRandomDate(),
#                        'TI', None, None, getRandomDate(), 'Incomplete']
#     add_data('exchanges', exchange_params)
#
#     exchange_params = ['920228342', '920228016', getRandomMeal(), getRandomDate(),
#                        'TI', getRandomDate(), 'Quad', getRandomDate(), 'Complete']
#     add_data('exchanges', exchange_params)
#
#     exchange_params = ['920228342', '920228016', getRandomMeal(), getRandomDate(),
#                        'TI', getRandomDate(), 'Quad', getRandomDate(), 'Complete']
#     add_data('exchanges', exchange_params)


if __name__ == '__main__':
    main()
    #add_ellen_and_shayna_exchanges()

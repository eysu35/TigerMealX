from datetime import date
from datetime import datetime
from database import db_access
import random


class Exchanges:

    # returns current exchanges for studentid as a list of Exchange objects
    # can take string or integer PUID
    @classmethod
    def get_current_exchanges(cls, studentid):
        current_exchanges = []
        # access the database here and assemble a list of Exchange objects
        # how is status encoded?
        stmt = f'''SELECT meal_exchange_id, student1_puid, 
        student2_puid, 
        meal, exchange1_date, exchange1_location_id, exchange2_date,
        exchange2_location_id, expiration_date, status FROM exchanges 
        WHERE (student1_puid=\'{studentid}\' OR student2_puid=\'
        {studentid}\') AND status=\'Incomplete\''''

        rows = db_access.fetchall(stmt)
        for row in rows:
            if row is None:
                return None

            puid1 = row[1]
            puid2 = row[2]

            stmt_std1_name = f'''SELECT student_name FROM 
            students WHERE puid=\'{puid1}\''''
            std1_name = db_access.fetch_first_val(stmt_std1_name)

            stmt_std2_name = f'''SELECT student_name FROM 
            students WHERE puid=\'{puid2}\''''
            std2_name = db_access.fetch_first_val(stmt_std2_name)

            exch_obj = Exchange(row[1], std1_name, row[2], std2_name, row[3], row[4], row[5], row[6],
                                row[7], row[8], row[9])
            current_exchanges.append(exch_obj)

        return current_exchanges

    # returns past exchanges for studentid as a list of Exchange objects
    @classmethod
    def get_past_exchanges(cls, studentid):
        # access the database here and assemble a list of Exchange objects
        past_exchanges = []
        # access the database here and assemble a list of Exchange objects
        stmt = f'''SELECT meal_exchange_id, student1_puid, 
        student2_puid, 
        meal, exchange1_date, exchange1_location_id, exchange2_date,
        exchange2_location_id, expiration_date, status FROM exchanges 
        WHERE (student1_puid=\'{studentid}\' OR student2_puid=\'
        {studentid}\') AND status =\'Complete\''''

        rows = db_access.fetchall(stmt)

        for row in rows:
            if row is None:
                return None

            puid1 = row[1]
            puid2 = row[2]

            stmt_std1_name = f'''SELECT student_name FROM 
            students WHERE puid=\'{puid1}\''''
            std1_name = db_access.fetch_first_val(stmt_std1_name)

            stmt_std2_name = f'''SELECT student_name FROM 
            students WHERE puid=\'{puid2}\''''
            std2_name = db_access.fetch_first_val(stmt_std2_name)

            exch_obj = Exchange(row[1], std1_name, row[2], std2_name, row[3], row[4], row[5], row[6],
                                row[7], row[8], row[9])
            past_exchanges.append(exch_obj)

        return past_exchanges


    @classmethod
    def add_new_exchange(cls, puid1, puid2, meal):
        stmt = f'''SELECT student_name FROM students WHERE 
            puid=\'{puid1}\''''
        student1_name = db_access.fetch_first_val(stmt)

        stmt = f'''SELECT student_name FROM students WHERE 
            puid=\'{puid2}\''''
        student2_name = db_access.fetch_first_val(stmt)

        exchange = Exchange(None, puid1, student1_name,
                            puid2, student2_name,
                            meal, None, None, None, None,
                            str(date.today()), 'Incomplete')

        #### OK we dont need to generate this random int because the db will
        # do this automatically when we insert a row. ####
        stmt = '''INSERT INTO exchanges(student1_puid, 
        student2_puid, meal, exchange1_date, exchange1_location_id, 
        exchange2_date, exchange2_location_id, expiration_date, 
        status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''

        db_access.insert_data(stmt, exchange.to_ordered_tuple())

    @classmethod
    def remove_exchange(cls, meal_exchange_id):
        stmt = f'''DELETE FROM exchanges WHERE meal_exchange_id=
        \'{meal_exchange_id}\''''

        ### do we need to send the meal_exchange_id again? ###
        db_access.insert_data(stmt, meal_exchange_id)

    @classmethod
    def exchange_firstmeal(cls, meal_exchange_id,
                            exchange1_location_id,
                      time):
        exchange1_date = date.today()
        exp_date = exchange1_date + datetime.timedelta(days=30)
        # assume time is in the format HH:MM:SS
        hour = int(str(time).split(':')[0])
        ##min = int(str(time).split(':')[1]) ### do we need???
        ### CAN RESET THESE TIMES LATER
        if (7 < hour < 10):
            meal = 'breakfast'
        elif (11 < hour < 14):
            meal = 'lunch'
        elif (17 < hour < 22):
            meal = 'dinner'

        ### fix this to the right format of Values %s etc
        stmt=f'''UPDATE exchanges SET meal = \'{meal}\' 
        AND exchange1_date = \'{exchange1_date}\'
        AND exchange1_location_id = \'{exchange1_location_id}\' 
        AND expiration_date = \'{exp_date}\'
        WHERE meal_exchange_id=\'{meal_exchange_id}\''''

        db_access.insert_data(stmt, [exchange1_date, exchange1_location_id,
                         meal_exchange_id])

    @classmethod
    def exchange_secondmeal(cls, meal_exchange_id, exchange2_date,
                      exchange2_location_id, time):
        stmt = f'''SELECT student1_PUID, student2_PUID, 
        exchange1_location_id, meal'''
        puid1, puid2, exchange1_loc, meal = db_access.fetchall(stmt)

        ### NEED TO DO
        ### check to see exchange1 location matches one of the 2,
        # and location 2 id matches the other
        ### REALIZING THAT WE ALSO NEED TO DO THIS FOR FIRSTMEAL

        # Make sure that the students are exchanging during the
        # same meal
        hour = int(str(time).split(':')[0])
        ##min = int(str(time).split(':')[1]) ### do we need???
        ### CAN RESET THESE TIMES LATER
        if (7 < hour < 10):
            meal2 = 'breakfast'
        elif (11 < hour < 14):
            meal2 = 'lunch'
        elif (17 < hour < 22):
            meal2 = 'dinner'

        assert (meal2 == meal)

        stmt = f'''UPDATE exchanges SET exchange2_date = \'
        {exchange2_date}\' AND exchange2_location_id = \
        '{exchange2_location_id}\' 
        WHERE meal_exchange_id=\'{meal_exchange_id}\''''

        db_access.insert_data(stmt, [exchange2_date, exchange2_location_id,
                         meal_exchange_id])


# getters and setters unfinished
class Exchange:

    def __str__(self):
        return f'{self._mealx_id} and {self._name1} ({self._puid1}) ' \
               f'and {self._name2} ({self._puid2}) for {self._meal} ' \
               f'({self._status})'

    def __init__(self, puid1, name1, puid2, name2, meal,
                 exch1_date, exch1_loc, exch2_date, exch2_loc, exp, status, mealx_id=None):
        self._mealx_id = mealx_id
        self._puid1 = puid1
        self._puid2 = puid2
        self._name1 = name1
        self._name2 = name2
        self._meal = meal
        self._status = status
        self._exch1_date = exch1_date
        self._exch1_loc = exch1_loc
        self._exch2_date = exch2_date
        self._exch2_loc = exch2_loc
        self._exp = exp
        self._init_date = None

    # returns tuple of table info in order of table columns for use in insert statement
    def to_ordered_tuple(self):
        return self._mealx_id, self._puid1, self._puid2, self._meal, \
               self._exch1_date,\
               self._exch1_loc, self._exch2_date, self._exch2_loc, self._exp, self._status

    def get_mealx_id(self):
        return self._mealx_id

    def set_mealx_id(self, mealx_id):
        self._mealx_id = mealx_id

    def get_puid1(self):
        return self._puid1

    def set_puid1(self, puid1):
        self._puid1 = puid1

    def get_puid2(self):
        return self._puid2

    def set_puid2(self, puid2):
        self._puid2 = puid2

    def get_name1(self):
        return self._name1

    def set_name1(self, name1):
        self._name1 = name1

    def set_name2(self, name2):
        self._name2 = name2

    def get_name2(self):
        return self._name2

    def get_meal(self):
        return self._meal

    def set_meal(self, meal):
        self._meal = meal

    def get_exch1_loc(self):
        return self._exch1_loc

    def set_exch1_loc(self, exch1_loc):
        self._exch1_loc = exch1_loc

    def get_exch2_loc(self):
        return self._exch2_loc

    def set_exch2_loc(self, exch2_loc):
        self._exch2_loc = exch2_loc

    def get_exch1_date(self):
        return self._exch1_date

    def set_exch1_date(self, exch1_date):
        self._exch1_date = exch1_date

    def get_exch2_date(self):
        return self._exch2_date

    def set_exch2_date(self, exch2_date):
        self._exch2_date = exch2_date

    def get_status(self):
        return self._status

    def set_status(self, status):
        self._status = status

    def get_exp(self):
        return self._exp

    def set_exp(self, exp):
        self._exp = exp

    # def to_dict(self):
    #     return {'name': self._name, 'place': self._place,
    #         'meal': self._meal, 'status': self._status, 'exp': self._exp}

# -----------------------------------------------------------------------


def test():
    # exh = Exchanges.get_current_exchanges(112345678)
    # for e in exh:
    #     print(e)

    Exchanges.add_new_exchange('Shayna Maleson', 'Ellen Su', 'breakfast')


if __name__ == '__main__':
    test()

from datetime import date, datetime, timedelta
from database import db_access
import random


class Exchanges:

    # returns current exchanges for studentid as a list of Exchange objects
    # can take string or integer PUID
    @classmethod
    def get_current_exchanges(cls, studentid):
        current_exchanges = []
        # access the database here and assemble a list of Exchange objects
        stmt = f'''SELECT meal_exchange_id, student1_puid, student2_puid, meal, exchange1_date, exchange1_location_id, 
        exchange2_date, exchange2_location_id, expiration_date, status FROM exchanges 
        WHERE (student1_puid=\'{studentid}\' OR student2_puid=\'{studentid}\') AND status=\'Incomplete\''''

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

            exch_obj = Exchange(row[1], std1_name, row[2],
                                std2_name, row[3], row[4], row[5], row[6],
                                row[7], row[8], row[9], mealx_id=row[0])
            current_exchanges.append(exch_obj)

        return current_exchanges

    # returns past exchanges for studentid as a list of Exchange objects
    @classmethod
    def get_past_exchanges(cls, studentid):
        # access the database here and assemble a list of Exchange objects
        past_exchanges = []
        # access the database here and assemble a list of Exchange objects
        stmt = f'''SELECT meal_exchange_id, student1_puid, student2_puid, meal, exchange1_date, exchange1_location_id, 
        exchange2_date, exchange2_location_id, expiration_date, status FROM exchanges WHERE 
        (student1_puid=\'{studentid}\' OR student2_puid=\'{studentid}\') AND status=\'Complete\''''

        rows = db_access.fetchall(stmt)
        print('past exchanges: ', rows)

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

            exch_obj = Exchange(row[1], std1_name, row[2],
                                std2_name, row[3], row[4], row[5], row[6],
                                row[7], row[8], row[9], mealx_id=row[0])
            past_exchanges.append(exch_obj)
            print(past_exchanges)

        return past_exchanges

    @classmethod
    def add_new_exchange(cls, puid1, puid2):
        stmt = f'''SELECT student_name FROM students WHERE 
            puid=\'{puid1}\''''
        student1_name = db_access.fetch_first_val(stmt)

        stmt = f'''SELECT student_name FROM students WHERE 
            puid=\'{puid2}\''''
        student2_name = db_access.fetch_first_val(stmt)

        exchange = Exchange(puid1, student1_name,
                            puid2, student2_name,
                            None, None, None, None, None,
                            str(date.today()), 'Incomplete', mealx_id=None)

        stmt = '''INSERT INTO exchanges(student1_puid, 
        student2_puid, meal, exchange1_date, exchange1_location_id, 
        exchange2_date, exchange2_location_id, expiration_date, 
        status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''

        db_access.insert_data(stmt, exchange.to_ordered_tuple_without_mealx_id())

    @classmethod
    def remove_exchange(cls, meal_exchange_id):
        stmt = f'''DELETE FROM exchanges WHERE meal_exchange_id=
        \'{meal_exchange_id}\''''

        db_access.execute(stmt)

    @classmethod
    def check_valid_exchange(cls, puid1, puid2, location_id, time):

        stmt = f'''SELECT meal_exchange_id, meal, exchange1_date, 
        exchange1_location_id, exchange2_date, exchange2_location_id, 
        status FROM exchanges WHERE ((student1_puid = \'{puid1}\' AND 
        student2_puid =  \'{puid2}\') OR (student1_puid = \'{puid2}\' AND 
        student2_puid =  \'{puid1}\')) AND status = \'Incomplete\' 
        ORDER BY expiration_date ASC'''

        #No exchanges between these students
        exchanges = db_access.fetchall(stmt)
        if len(exchanges) == 0:
            return False, "No open exchange between these students."

        # check that both students have valid plans and the location
        # matches one of their locations
        stmt = f'''SELECT puid, netid, student_name, meal_plan_id, 
        is_valid_for_meal_exchange FROM students WHERE puid = \'{puid1}\''''
        student1 = db_access.fetchone(stmt)
        stmt = f'''SELECT puid, netid, student_name, 
        meal_plan_id, is_valid_for_meal_exchange FROM students WHERE puid = \'{puid2}\''''
        student2 = db_access.fetchone(stmt)

        # check if both students have valid plans for exchange
        if (not student1[4] or not student2[4]):
            return False, "Student plan unable to exchange."

        # check if location_id matches one of student plans
        stmt = f'''SELECT location_id FROM student_plans WHERE
                meal_plan_id = \'{student1[3]}\''''
        loc1_id = db_access.fetch_first_val(stmt)

        stmt = f'''SELECT location_id FROM student_plans WHERE
                   meal_plan_id = \'{student2[3]}\''''
        loc2_id = db_access.fetch_first_val(stmt)

        if ((location_id != loc1_id) and (location_id != loc2_id)):
            return False, "Invalid location for students to exchange meal."

        # determine which meal based on time
        hour = int(str(time).split(':')[0])
        if (7 < hour < 10):
            meal = 'breakfast'
        elif (11 < hour < 14):
            meal = 'lunch'
        elif (17 < hour < 22):
            meal = 'dinner'
        # error handling
        else: meal = None

        # at this point, validated open exchange between student 1
        # and student 2. Determine if attempting to exchange for the
        # first or second time, send to relevant method

        valid_exchange_id = None
        for exchange in exchanges:
            exchange_id = exchange[0]
            # if first exchange time is none, neither meal has been
            # completed, initiate first exchange
            if exchange[2] is None:
                Exchanges.update_meal1(exchange_id, location_id, meal)
                return True, "Exchange successfully updated!"

            # if first exchange has been completed, check right meal and
            # un-exchanged location
            if (exchange[1] == meal) and (exchange[3] != location_id):
                valid_exchange_id = exchange_id

        if valid_exchange_id is None:
            return False, "Students exchanging for wrong meal or " \
                          "wrong location."

        Exchanges.update_meal2(valid_exchange_id, location_id)
        return True, "Exchange successfully updated!"

    # sets meal 1 info for a validated exchange
    @classmethod
    def update_meal1(cls, mealx_id, location_id, meal):
        exchange1_date = date.today()
        exp_date = exchange1_date + timedelta(days=30)

        stmt = f'''UPDATE exchanges SET meal = \'{meal}\', 
        exchange1_date = \'{exchange1_date}\', 
        exchange1_location_id = \'{location_id}\',
        expiration_date = \'{exp_date}\',
        WHERE meal_exchange_id=\'{mealx_id}\''''

        db_access.execute_stmt(stmt)

    @classmethod
    def update_meal2(cls, mealx_id, location_id):
        exchange2_date = date.today()

        stmt = f'''UPDATE exchanges SET 
        exchange2_date = \'{exchange2_date}\', 
        exchange2_location_id = \'{location_id}\'
        WHERE meal_exchange_id=\'{mealx_id}\''''

        db_access.execute(stmt)

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

    # returns tuple of table info in order of table columns without mealxid
    def to_ordered_tuple_without_mealx_id(self):
        return self._puid1, self._puid2, self._meal, \
               self._exch1_date, \
               self._exch1_loc, self._exch2_date, self._exch2_loc, self._exp, self._status

    # returns tuple of table info in order of table columns for use in insert statement
    def to_ordered_tuple(self):
        return self._mealx_id, self._puid1, self._puid2, self._meal, \
               self._exch1_date, \
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

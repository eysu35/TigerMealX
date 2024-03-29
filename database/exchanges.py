from datetime import datetime, date, timedelta, time
from database import db_access
import re


class Exchanges:

    # get location name from location id
    @classmethod
    def get_loc_name_from_id(cls, loc_id):
        stmt = f'''SELECT location_name FROM locations WHERE 
        location_id = \'{loc_id}\''''
        name = db_access.fetch_first_val(stmt)
        return name

    @classmethod
    def get_plan_from_puid(cls, puid):
        stmt = f'''SELECT meal_plan_id FROM students WHERE puid=\'{puid}\''''
        meal_plan_id = db_access.fetch_first_val(stmt)

        stmt = f'''SELECT location_id FROM student_plans WHERE meal_plan_id = \'{meal_plan_id}\''''
        loc_id = db_access.fetch_first_val(stmt)

        stmt = f'''SELECT location_name FROM locations WHERE location_id = \'{loc_id}\''''
        loc_name = db_access.fetch_first_val(stmt)
        return loc_name

    # returns current exchanges for studentid as a list of Exchange objects
    # can take string or integer PUID
    @classmethod
    def get_current_exchanges(cls, studentid):
        current_exchanges = []
        # access the database here and assemble a list of Exchange objects
        stmt = f'''SELECT meal_exchange_id, student1_puid, student2_puid, meal, exchange1_date, exchange1_location_id, 
        exchange2_date, exchange2_location_id, expiration_date, status FROM exchanges 
        WHERE (student1_puid=\'{studentid}\' OR student2_puid=\'{studentid}\') 
        AND status=\'Incomplete\' ORDER BY expiration_date'''

        rows = db_access.fetchall(stmt)
        for row in rows:
            if row is None:
                return None

            puid1 = row[1]
            puid2 = row[2]

            student1_loc = Exchanges.get_plan_from_puid(puid1)
            student2_loc = Exchanges.get_plan_from_puid(puid2)


            stmt_std1_name = f'''SELECT student_name FROM 
            students WHERE puid=\'{puid1}\''''
            std1_name = db_access.fetch_first_val(stmt_std1_name)

            stmt_std2_name = f'''SELECT student_name FROM 
            students WHERE puid=\'{puid2}\''''
            std2_name = db_access.fetch_first_val(stmt_std2_name)

            # verify that the expiration date of the exchange is not
            # past today's date
            if row[8] < date.today():
                continue

            exch_obj = Exchange(row[1], std1_name, row[2],
                                std2_name, row[3], row[4], row[5], row[6],
                                row[7], row[8], row[9],
                                student1_loc, student2_loc,
                                mealx_id=row[0])
            current_exchanges.append(exch_obj)

        return current_exchanges

    # returns past exchanges for studentid as a list of Exchange objects
    @classmethod
    def get_past_exchanges(cls, studentid):
        # access the database here and assemble a list of Exchange objects
        past_exchanges = []
        # access the database here and assemble a list of Exchange objects
        stmt = f'''SELECT meal_exchange_id, student1_puid, student2_puid, meal, exchange1_date, exchange1_location_id, 
        exchange2_date, exchange2_location_id, expiration_date, status FROM exchanges 
        WHERE (student1_puid=\'{studentid}\' OR student2_puid=\'{studentid}\') 
        AND (status=\'Complete\' OR status=\'Expired\' OR status=\'Unused\') ORDER BY exchange2_date'''

        rows = db_access.fetchall(stmt)

        for row in rows:
            if row is None:
                return None

            puid1 = row[1]
            puid2 = row[2]

            student1_loc = Exchanges.get_plan_from_puid(puid1)
            student2_loc = Exchanges.get_plan_from_puid(puid2)

            stmt_std1_name = f'''SELECT student_name FROM 
            students WHERE puid=\'{puid1}\''''
            std1_name = db_access.fetch_first_val(stmt_std1_name)

            stmt_std2_name = f'''SELECT student_name FROM 
            students WHERE puid=\'{puid2}\''''
            std2_name = db_access.fetch_first_val(stmt_std2_name)

            exch_obj = Exchange(row[1], std1_name, row[2],
                                std2_name, row[3], row[4], row[5], row[6],
                                row[7], row[8], row[9],
                                student1_loc, student2_loc,
                                mealx_id=row[0])
            past_exchanges.append(exch_obj)

        return past_exchanges

    @classmethod
    def add_new_exchange(cls, puid1, puid2):
        stmt = f'''SELECT student_name FROM students WHERE 
            puid=\'{puid1}\''''
        student1_name = db_access.fetch_first_val(stmt)

        stmt = f'''SELECT student_name FROM students WHERE 
            puid=\'{puid2}\''''
        student2_name = db_access.fetch_first_val(stmt)
        exp_date = date.today() + timedelta(days=30)

        student1_loc = Exchanges.get_plan_from_puid(puid1)
        print(student1_loc)

        student2_loc = Exchanges.get_plan_from_puid(puid2)
        print(student2_loc)
        exchange = Exchange(puid1, student1_name,
                            puid2, student2_name,
                            None, None, None, None, None,
                            str(exp_date), 'Incomplete',
                            student1_loc, student2_loc, mealx_id=None)

        stmt = '''INSERT INTO exchanges(student1_puid, 
        student2_puid, meal, exchange1_date, exchange1_location_id, 
        exchange2_date, exchange2_location_id, expiration_date, 
        status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''

        db_access.insert_data(stmt, exchange.to_ordered_tuple_without_mealx_id())

    @classmethod
    def remove_exchange(cls, meal_exchange_id):
        stmt = f'''DELETE FROM exchanges WHERE meal_exchange_id=
        \'{meal_exchange_id}\''''

        db_access.execute_stmt(stmt)

    # public method that validates the existence of an exchange between the
    # students and updates the first or second meal accordingly
    # returns (boolean success, error msg)
    @classmethod
    def update_exchange(cls, puid1, puid2, location_id, meal_time):
        regex = re.compile(r'[0-2][0-9]:[0-5][0-9]')
        if not regex.fullmatch(meal_time.strip()):
            return False, 'Invalid time'

        stmt = f'''SELECT meal_exchange_id, meal, exchange1_date, 
        exchange1_location_id, exchange2_date, exchange2_location_id, 
        status FROM exchanges WHERE ((student1_puid = \'{puid1}\' AND 
        student2_puid =  \'{puid2}\') OR (student1_puid = \'{puid2}\' AND 
        student2_puid =  \'{puid1}\')) AND status = \'Incomplete\' 
        ORDER BY expiration_date ASC'''

        # No exchanges between these students
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
        if not student1[4] or not student2[4]:
            return False, "Student plan unable to exchange."

        # check if location_id matches one of student plans
        stmt = f'''SELECT location_id FROM student_plans WHERE
                meal_plan_id = \'{student1[3]}\''''
        loc1_id = db_access.fetch_first_val(stmt)

        stmt = f'''SELECT location_id FROM student_plans WHERE
                   meal_plan_id = \'{student2[3]}\''''
        loc2_id = db_access.fetch_first_val(stmt)

        if location_id != loc1_id and location_id != loc2_id:
            return False, "Invalid location for students to exchange meal."

        # determine which meal based on time
        hour = int(str(meal_time).split(':')[0])
        if not (0 <= hour <= 23):
            return False, 'Invalid time'
        min = int(str(meal_time).split(':')[1])
        if not (0 <= min <= 59):
            return False, 'Invalid time'
        meal_time = time(hour, min, 0)
        if time(6,30,0) <= meal_time <= time(11,10,0):
            meal = 'breakfast'
        elif time(11,15,0) <= meal_time <= time(15,0,0):
            meal = 'lunch'
        elif time(15,10,0) <= meal_time <= time(22,0,0):
            meal = 'dinner'
        else:
            return False, 'Not a valid meal time.'

        # at this point, validated open exchange between student 1
        # and student 2. Determine if attempting to exchange for the
        # first or second time, send to relevant method
        msg = "Exchange error"

        valid_exchange_id = None
        set_first_meal = False
        first_meal_exchange_id = None
        meal_today_already_exists = False
        for exchange in exchanges:
            exchange_id = exchange[0]
            # if first exchange time is none, neither meal has been
            # completed, initiate first exchange
            if exchange[2] is None:
                set_first_meal = True
                first_meal_exchange_id = exchange_id

            # for partially completed exchanges
            if exchange[1] == meal:  # if correct meal

                if date.today() == exchange[2]:
                    meal_today_already_exists = True

                if exchange[3] != location_id:
                    valid_exchange_id = exchange_id
                else:
                    msg = "Students have already exchanged at this location for this swap."
            else:  # wrong meal
                if exchange[3] != location_id:  # but correct location
                    msg = "No exchange open between these students for this meal time."
                else:
                    msg = 'No exchange open between these students for this meal time at this location.'

        if set_first_meal and valid_exchange_id is None:
            if not meal_today_already_exists:
                Exchanges._update_meal1(first_meal_exchange_id, location_id, meal)
                return True, "Exchange successfully updated!"
            else:
                return False, "Students have already exchanged for this meal today."

        if valid_exchange_id is None:
            return False, msg

        # if meal_today_already_exists:
        #     return False, "Students have already exchanged for this meal today."

        Exchanges._update_meal2(valid_exchange_id, location_id)
        return True, "Exchange successfully updated!"

    # sets meal 1 info for a validated exchange
    @classmethod
    def _update_meal1(cls, mealx_id, location_id, meal):
        exchange1_date = date.today()
        exp_date = exchange1_date + timedelta(days=30)

        stmt = f'''UPDATE exchanges SET meal = \'{meal}\', 
        exchange1_date = \'{exchange1_date}\', 
        exchange1_location_id = \'{location_id}\',
        expiration_date = \'{exp_date}\' WHERE meal_exchange_id=\'{mealx_id}\''''

        db_access.execute_stmt(stmt)

    # sets meal 2 info, mark exchange as complete
    @classmethod
    def _update_meal2(cls, mealx_id, location_id):
        exchange2_date = date.today()

        stmt = f'''UPDATE exchanges SET 
        exchange2_date = \'{exchange2_date}\', 
        exchange2_location_id = \'{location_id}\',
        status = \'Complete\'
        WHERE meal_exchange_id=\'{mealx_id}\''''

        db_access.execute_stmt(stmt)

    # regularly comb through exchanges to check dates and set
    # exchange objects statuses accordingly
    @classmethod
    def update_exchange_status(cls):
        today = date.today()
        stmt = f'''SELECT meal_exchange_id, expiration_date, 
        exchange1_date FROM exchanges WHERE status = \'Incomplete\''''

        exchanges = db_access.fetchall(stmt)

        one_week = []
        three_days = []
        expired = []
        for exchange in exchanges:
            mealx_id = exchange[0]
            exp_date = exchange[1]
            exchange1_date = exchange[2]

            # mark any exchanges with expiration dates that have
            # passed as an expired exchange
            if exp_date > today:
                stmt = f'''UPDATE exchanges SET status = \'Expired\'
                        WHERE meal_exchange_id=\'{mealx_id}\''''
                db_access.execute_stmt(stmt)
                expired.append(mealx_id)

            # mark any exchanges that have not been used within the
            # first five days as an unused exchange to clean table
            if (exp_date == (today + timedelta(days=25))) and \
                    (exchange1_date is None):
                stmt = f'''UPDATE exchanges SET status = \'Unused\'
                        WHERE meal_exchange_id=\'{mealx_id}\''''
                db_access.execute_stmt(stmt)

            # send any exchanges that are about to expire back
            if exp_date == (today + timedelta(days=7)):
                one_week.append(mealx_id)

            if exp_date == (today + timedelta(days=3)):
                three_days.append(mealx_id)

        # return all exchanges that are expired or about to expire in
        # one week or in 3 days
        return (expired, one_week, three_days)

    # return netids of 2 students given the mealx_id
    @classmethod
    def get_netid_from_mealx_id(cls, mealx_id):
        stmt = f'''SELECT student1_puid, student2_puid FROM exchanges 
        WHERE meal_exchange_id = \'{mealx_id}\''''
        puid1, puid2 = db_access.fetchone(stmt)

        stmt = f'''SELECT netid FROM students WHERE puid = 
        \'{puid1}\''''
        netid1 = db_access.fetch_first_val(stmt)

        stmt = f'''SELECT netid FROM students WHERE puid = 
                \'{puid2}\''''
        netid2 = db_access.fetch_first_val(stmt)

        return(netid1, netid2)

    @classmethod
    def get_loc_id_from_loc_name(cls, loc_name):
        stmt = f'''SELECT location_id FROM locations WHERE LOWER(location_name)=LOWER(\'{loc_name}\')'''
        loc_id = db_access.fetch_first_val(stmt)
        return loc_id


# getters and setters unfinished
class Exchange:

    def __str__(self):
        return f'{self._mealx_id} and {self._name1} ({self._puid1}) ' \
               f'and {self._name2} ({self._puid2}) for {self._meal} ' \
               f'({self._status})'

    def __init__(self, puid1, name1, puid2, name2,
                 meal,
                 exch1_date, exch1_loc_id, exch2_date, exch2_loc_id,
                 exp, status, student1_loc, student2_loc,
                 mealx_id=None):
        self._mealx_id = mealx_id
        self._puid1 = puid1
        self._puid2 = puid2
        self._name1 = name1
        self._name2 = name2
        self._student1_loc = student1_loc
        self._student2_loc = student2_loc
        self._meal = meal
        self._status = status
        self._exch1_date = exch1_date
        self._exch1_loc_id = exch1_loc_id
        self._exch2_date = exch2_date
        self._exch2_loc_id = exch2_loc_id
        self._exp = exp

    # returns tuple of table info in order of table columns without mealxid
    def to_ordered_tuple_without_mealx_id(self):
        return self._puid1, self._puid2, self._meal, \
               self._exch1_date, \
               self._exch1_loc_id, self._exch2_date, \
               self._exch2_loc_id, \
               self._exp, self._status

    # returns tuple of table info in order of table columns for use in insert statement
    def to_ordered_tuple(self):
        return self._mealx_id, self._puid1, self._puid2, self._meal, \
               self._exch1_date, \
               self._exch1_loc_id, self._exch2_date, \
               self._exch2_loc_id, \
               self._exp, self._status
    
    def get_daysleft(self):
        daysleft = abs((self._exp - date.today()).days)
        return daysleft

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

    def get_student1_loc(self):
        return self._student1_loc

    def set_student1_loc(self, student1_loc):
        self._student1_loc = student1_loc

    def get_student2_loc(self):
        return self._student2_loc

    def set_student2_loc(self, student2_loc):
        self._student2_loc = student2_loc

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

    def get_exch1_loc_id(self):
        return self._exch1_loc_id

    def set_exch1_loc_id(self, exch1_loc_id):
        self._exch1_loc_id = exch1_loc_id

    # get name
    def get_exch1_loc_name(self):
        if self._exch1_loc_id is None:
            return None
        return Exchanges.get_loc_name_from_id(self._exch1_loc_id)

    def get_exch2_loc_id(self):
        return self._exch2_loc_id

    def set_exch2_loc_id(self, exch2_loc_id):
        self._exch2_loc_id = exch2_loc_id

    # get name
    def get_exch2_loc_name(self):
        if self._exch2_loc_id is None:
            return None
        return Exchanges.get_loc_name_from_id(self._exch2_loc_id)

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

    # get the name of the other person given the user's puid
    def get_display_name_from_puid(self, puid):
        if puid == self._puid1:
            return self._name2
        else:
            return self._name1

    # def to_dict(self):
    #     return {'name': self._name, 'place': self._place,
    #         'meal': self._meal, 'status': self._status, 'exp': self._exp}


# -----------------------------------------------------------------------


def test():
    # exh = Exchanges.get_current_exchanges(112345678)
    # for e in exh:
    #     print(e)
    pass


if __name__ == '__main__':
    test()

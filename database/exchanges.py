from config import config
import psycopg2
import random


# returns the cursor
def db_execute_fetchone(stmt):
    try:
        # connection establishment
        params = config()
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(stmt)
        return cur.fetchone()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("success")


def db_insert(stmt, data):
    try:
        # connection establishment
        params = config()
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(stmt, data)
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("success")


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

        try:
            # connection establishment
            params = config()
            conn = psycopg2.connect(**params)
            conn.autocommit = True
            cur = conn.cursor()

            cur.execute(stmt)

            for row in cur.fetchall():
                if row == None:
                    return None

                puid1 = row[1]
                puid2 = row[2]
                stmt_std1_name = f'''SELECT student_name FROM 
                students WHERE puid=\'{puid1}\''''
                cur.execute(stmt_std1_name)
                std1_name = cur.fetchone()[0]

                stmt_std2_name = f'''SELECT student_name FROM 
                students WHERE puid=\'{puid2}\''''
                cur.execute(stmt_std2_name)
                std2_name = cur.fetchone()[0]

                ###  PUT ROW[0] IN LATER AS OPTIONAL ARG
                exch_obj = Exchange(row[1], std1_name, row[2], std2_name, row[3], row[4], row[5], row[6],
                                    row[7], row[8], row[9])
                current_exchanges.append(exch_obj)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print("success")

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

        try:
            # connection establishment
            params = config()
            conn = psycopg2.connect(**params)
            conn.autocommit = True
            cur = conn.cursor()

            cur.execute(stmt)

            for row in cur.fetchall():
                if row == None:
                    return None
                puid1 = row[1]
                puid2 = row[2]
                stmt_std1_name = f'''SELECT student_name FROM 
                students WHERE puid=\'{puid1}\''''
                cur.execute(stmt_std1_name)
                std1_name = cur.fetchone()[0]

                stmt_std2_name = f'''SELECT student_name FROM 
                students WHERE puid=\'{puid2}\''''
                cur.execute(stmt_std2_name)
                std2_name = cur.fetchone()[0]

                ###  PUT ROW[0] IN LATER AS OPTIONAL ARG
                exch_obj = Exchange(row[1], std1_name, row[2], std2_name, row[3], row[4], row[5], row[6],
                                    row[7], row[8], row[9])
                past_exchanges.append(exch_obj)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print("success")
                # print("past")

        return past_exchanges

    @classmethod
    def add_new_exchange(cls, puid1, puid2, meal):
        # # get puids
        # stmt = f'''SELECT puid FROM students WHERE student_name=LOWER(\
        # '{student1_name}\')'''
        # result = db_execute_fetchone(stmt)
        # puid1 = result[0]
        #
        # stmt = f'''SELECT puid FROM students WHERE student_name=LOWER(\
        # '{student2_name}\')'''
        # result = db_execute_fetchone(stmt)
        # puid2 = result[0]

        stmt = f'''SELECT student_name FROM students WHERE puid=\'{puid1}\''''
        result = db_execute_fetchone(stmt)
        student1_name = result[0]

        stmt = f'''SELECT student_name FROM students WHERE puid=\'{puid2}\''''
        result = db_execute_fetchone(stmt)
        student2_name = result[0]

        exchange = Exchange(puid1, student1_name,
                            puid2, student2_name,
                            meal, None, None, None, None, '2022-02-10',
                            'Incomplete')

        #### OK we dont need to generate this random int because the db will
        # do this automatically when we insert a row. ####
        stmt = '''INSERT INTO exchanges(student1_puid, 
        student2_puid, meal, exchange1_date, exchange1_location_id, 
        exchange2_date, exchange2_location_id, expiration_date, 
        status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''

        db_insert(stmt, exchange.to_ordered_tuple())

    @classmethod
    def remove_exchange(cls, meal_exchange_id):
        stmt = f'''DELETE FROM exchanges WHERE meal_exchange_id=
        \'{meal_exchange_id}\''''

        ### do we need to send the meal_exchange_id again? ###
        db_insert(stmt, meal_exchange_id)

    @classmethod
    def add_exchange1(cls, meal_exchange_id, exchange1_date,
                   exchange1_location_id):

        stmt=f'''UPDATE exchanges SET exchange1_date = \'
        {exchange1_date}\' AND exchange1_location_id = \
        '{exchange1_location_id}\' 
        WHERE meal_exchange_id=\'{meal_exchange_id}\''''

        db_insert(stmt, [exchange1_date, exchange1_location_id,
                         meal_exchange_id])

    #### separate method or just combine w some string concatenation
    # for the numbers??? ######
    # wtf ?/ where does the meal exchange ID come from
    @classmethod
    def add_exchange2(cls, meal_exchange_id, exchange2_date,
                      exchange2_location_id):
        stmt = f'''UPDATE exchanges SET exchange2_date = \'
        {exchange2_date}\' AND exchange2_location_id = \
        '{exchange2_location_id}\' 
        WHERE meal_exchange_id=\'{meal_exchange_id}\''''

        db_insert(stmt, [exchange2_date, exchange2_location_id,
                         meal_exchange_id])

# getters and setters unfinished
class Exchange:

    def __str__(self):
        return f'{self._name1} ({self._puid1}) and {self._name2} ({self._puid2}) for {self._meal} ({self._status})'

    def __init__(self, puid1, name1, puid2, name2, meal,
                 exch1_date, exch1_loc, exch2_date, exch2_loc, exp, status):
        # self._mealx_id = mealx_id
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
        return self._puid1, self._puid2, self._meal, self._exch1_date,\
               self._exch1_loc, self._exch2_date, self._exch2_loc, self._exp, self._status

    # def get_mealx_id(self):
    #     return self._mealx_id
    #
    # def set_mealx_id(self, mealx_id):
    #     self._mealx_id = mealx_id

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

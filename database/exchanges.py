from config import config
import psycopg2


class CurrentExchanges:

    # returns current exchanges for studentid as a list of Exchange objects
    @classmethod
    def get(cls, studentid):
        current_exchanges = []
        # access the database here and assemble a list of Exchange objects
        # how is status encoded?
        stmt = f'''SELECT mealx_id, stdnt1_PUID, stdnt2_PUID, meal, exchge1_date, exchge1_loc, exchge2_date,
         exchge2_loc, exp_date, status FROM exchanges WHERE stdnt1_PUID={studentid} OR stdnt2_PUID={studentid}
        AND status=\'Incomplete\''''

        try:
            # connection establishment
            params = config()
            conn = psycopg2.connect(**params)
            conn.autocommit = True
            cur = conn.cursor()

            cur.execute(stmt)
            for row in cur.fetchall():
                puid1 = row[1]
                puid2 = row[2]
                stmt_std1_name = f'''SELECT student_name FROM students WHERE puid={puid1}'''
                cur.execute(stmt_std1_name)
                std1_name = cur.fetchone()[0]

                stmt_std2_name = f'''SELECT student_name FROM students WHERE puid={puid2}'''
                cur.execute(stmt_std2_name)
                std2_name = cur.fetchone()[0]

                exch_obj = Exchange(row[0], row[1], std1_name, row[2], std2_name, row[3], row[4], row[5], row[6],
                                    row[7], row[8], row[9])
                current_exchanges.append(exch_obj)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print("success")


class PastExchanges:

    # returns past exchanges for studentid as a list of Exchange objects
    # requires postgres connection as arg
    @classmethod
    def get(cls, connection, studentid):
        pass
        # access the database here and assemble a list of Exchange objects


# getters and setters unfinished
# this also breaks exchanges.html
class Exchange:

    def __init__(self, mealx_id, puid1, name1, puid2, name2, meal,
                 exch1_date, exch1_loc, exch2_date, exch2_loc, exp, status):
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

def _test():
    book = Book('Kernighan', 'The Practice of Programming', 40.74)
    print(book.to_tuple())
    print()
    print(book.to_xml())
    print()
    print(book.to_dict())

if __name__ == '__main__':
    _test()

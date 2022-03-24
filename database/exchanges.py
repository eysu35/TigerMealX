from config import config
import psycopg2


class CurrentExchanges:
    # _connection = None

    # def __init__(self, db_conn):
    #     CurrentExchanges._connection = db_conn

    # returns current exchanges for studentid as a list of Exchange objects
    # requires postgres connection as arg
    @classmethod
    def get(cls, connection, studentid):
        pass
        # access the database here and assemble a list of Exchange objects


class PastExchanges:

    # returns past exchanges for studentid as a list of Exchange objects
    # requires postgres connection as arg
    @classmethod
    def get(cls, connection, studentid):
        pass
        # access the database here and assemble a list of Exchange objects


class Exchange:

    def __init__(self, name, place, meal, status, exp):
        self._name = name
        self._meal = meal
        self._place = place
        self._status = status
        self._exp = exp

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name
        
    def get_place(self):
        return self._place

    def set_place(self, place):
        self._place = place

    def get_meal(self):
        return self._meal

    def set_meal(self, meal):
        self._meal = meal

    def get_status(self):
        return self._status

    def set_status(self, status):
        self._status = status

    def get_exp(self):
        return self._exp

    def set_exp(self, exp):
        self._exp = exp

    def to_dict(self):
        return {'name': self._name, 'place': self._place,
            'meal': self._meal, 'status': self._status, 'exp': self._exp}

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


class Exchange:

    def __init__(self, name, place, meal, status, exp):
        self._name = name
        self._meal = meal
        self._place = place
        self._status = status
        self._exp = exp

    def get_name(self):
        return self._name
        
    def get_place(self):
        return self._place
    def get_meal(self):
        return self._meal
    def get_status(self):
        return self._status
    def get_date(self):
        return self._exp

   


    def to_dict(self):
        return {'author': self._author, 'title': self._title,
            'price': self._price}

#-----------------------------------------------------------------------

def _test():
    book = Book('Kernighan', 'The Practice of Programming', 40.74)
    print(book.to_tuple())
    print()
    print(book.to_xml())
    print()
    print(book.to_dict())

if __name__ == '__main__':
    _test()

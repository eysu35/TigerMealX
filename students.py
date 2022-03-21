from config import config
import psycopg2


# container class for students
class Students:

    @classmethod
    def get_puid_from_name(cls, name):
        str_name = str(name)
        stmt = f'''SELECT PUID FROM students WHERE student_name LIKE \'%{str_name}%\''''
        puid = None

        try:
            # connection establishment
            conn = psycopg2.connect(
                database="mealx",
                user='postgres',
                password='HelloPGDB',
                host='localhost',
                port='5432')

            conn.autocommit = True
            cur = conn.cursor()

            cur.execute(stmt)
            puid = cur.fetchone()[0]

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print("success")

        return puid

    @classmethod
    def search_students_by_name(cls, name):
        str_name = str(name)
        stmt = f'''SELECT student_name FROM students WHERE student_name LIKE \'%{str_name}%\''''
        students = []

        try:
            # connection establishment
            conn = psycopg2.connect(
                database="mealx",
                user='postgres',
                password='HelloPGDB',
                host='localhost',
                port='5432')

            conn.autocommit = True
            cur = conn.cursor()

            cur.execute(stmt)
            results = cur.fetchall()
            for result in results:
                student = Student(None, result[0], None)
                students.append(student)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print("success")

        return students


    # returns list of Student objects that are friends of the given puid
    @classmethod
    def get_friend_names(cls, puid):
        # build the sql statement
        stmt = f"""SELECT friend_PUID FROM friends WHERE PUID={puid}"""

        friend_data = []

        try:
            # connection establishment
            conn = psycopg2.connect(
                database="mealx",
                user='postgres',
                password='HelloPGDB',
                host='localhost',
                port='5432')

            conn.autocommit = True
            cur = conn.cursor()

            cur.execute(stmt)
            friend_puids = cur.fetchall()  # why are these tuples with one thing in them
            # print(friend_puids)

            for friend_puid in friend_puids:
                actual_puid = friend_puid[0]
                # print(actual_puid)
                stmt2 = f"""SELECT student_name, meal_plan FROM students WHERE PUID={actual_puid}"""
                cur.execute(stmt2)
                row = cur.fetchone()

                student = Student(actual_puid, row[0], row[1])
                # print(student)
                friend_data.append(student)

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

        return friend_data


class Student:

    def __init__(self, puid, name, club):
        self._puid = puid
        # self._netid = netid
        self._name = name
        self._club = club
        # self._mealplan = mealplan
        # self._location_id = location_id
        # other fields?

    def __str__(self):
        return f'{self._name}, {self._puid}, {self._club}'

    def get_puid(self):
        return self._puid

    def set_puid(self, puid):
        self._puid = puid

    # def get_netid(self):
    #     return self._netid

    # def set_netid(self, netid):
    #     self._netid = netid

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_club(self):
        return self._club

    def set_club(self, club):
        self._club = club


if __name__ == '__main__':
    Students.get_friend_names(123456789)
    print(Students.get_puid_from_name('Shayna'))
    result = Students.search_students_by_name('a')
    for item in result:
        print(item)

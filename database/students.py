from config import config
import psycopg2


# container class for students
class Students:

    @classmethod
    def get_name_from_netid(cls, netid):
        str_netid = str(netid)
        print(str_netid)
        stmt = f'''SELECT student_name FROM students WHERE 
        netid=\'{str_netid}\''''

        first_name = None

        try:
            # connection establishment
            params = config()
            conn = psycopg2.connect(**params)

            conn.autocommit = True
            cur = conn.cursor()

            cur.execute(stmt)
            first_name = cur.fetchone()[2]
            first_name = first_name.split(' ')[0]
            print(first_name)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print("success")

        return first_name

    @classmethod
    def get_puid_from_name(cls, name):
        str_name = str(name)
        stmt = f'''SELECT puid FROM students WHERE student_name LIKE 
            \'%{str_name}%\''''
        puid = None

        try:
            # connection establishment
            params = config()
            conn = psycopg2.connect(**params)

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
        stmt = f'''SELECT student_name FROM students WHERE 
        LOWER(student_name) LIKE LOWER(\'%{str_name}%\')'''
        students = []

        try:
            # connection establishment
            params = config()
            conn = psycopg2.connect(**params)

            conn.autocommit = True
            cur = conn.cursor()

            cur.execute(stmt)
            results = cur.fetchall()
            for result in results:
                student = Student(None, None, result[0], None)
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
        stmt = f"""SELECT friend_puid FROM friends WHERE puid={puid}"""

        friend_data = []

        try:
            # connection establishment
            params = config()
            conn = psycopg2.connect(**params)

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

    def __init__(self, puid, netid, name, mealplanid):
        self._puid = puid
        self._netid = netid
        self._name = name
        self._mealplanid = mealplanid
        # self._club = club
        # self._location_id = location_id
        # other fields?

    def __str__(self):
        return f'{self._puid}, {self._netid}, {self._name},' \
               f' {self._mealplanid}'

    def get_puid(self):
        return self._puid

    def set_puid(self, puid):
        self._puid = puid

    def get_netid(self):
        return self._netid

    def set_netid(self, netid):
        self._netid = netid

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_mealplanid(self):
        return self._mealplanid

    def set_mealplanid(self, mealplanid):
        self._club = mealplanid


if __name__ == '__main__':
    Students.get_friend_names(123456789)
    print(Students.get_puid_from_name('Shayna'))
    result = Students.search_students_by_name('a')
    for item in result:
        print(item)

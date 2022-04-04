from config import config
import psycopg2


# container class for students
class Students:

    # takes a puid as integer or string, puid should come from validated list of students (puid must already exist in db)
    @classmethod
    def get_student_by_puid(cls, puid):
        str_puid = str(puid).strip()
        stmt = f'''SELECT puid, netid, student_name, meal_plan_id, isvalidformealexchange FROM students WHERE 
                puid=\'{str_puid}\''''
        student = None

        try:
            # connection establishment
            params = config()
            conn = psycopg2.connect(**params)

            conn.autocommit = True
            cur = conn.cursor()

            cur.execute(stmt)
            res = cur.fetchone()
            student = Student(res[0], res[1], res[2], res[3], res[4])

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print("success")

        return student


    @classmethod
    def get_first_name_from_netid(cls, netid):
        str_netid = str(netid).strip()
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
            first_name = cur.fetchone()[0]
            first_name = first_name.split(' ')[0]

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print("success")

        return first_name

    # @classmethod
    # def get_puid_from_name(cls, name):
    #     str_name = str(name)
    #     stmt = f'''SELECT puid FROM students WHERE student_name LIKE
    #         \'%{str_name}%\''''
    #     puid = None
    #
    #     try:
    #         # connection establishment
    #         params = config()
    #         conn = psycopg2.connect(**params)
    #
    #         conn.autocommit = True
    #         cur = conn.cursor()
    #
    #         cur.execute(stmt)
    #         puid = cur.fetchone()[0]
    #
    #     except (Exception, psycopg2.DatabaseError) as error:
    #         print(error)
    #     finally:
    #         if conn is not None:
    #             conn.close()
    #             print("success")
    #
    #     return puid

    @classmethod
    def get_puid_from_netid(cls, netid):
        str_netid = str(netid).strip()
        stmt = f'''SELECT puid FROM students WHERE netid=\'{str_netid}\''''
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
        stmt = f'''SELECT puid, netid, student_name, meal_plan_id, isvalidformealexchange FROM students WHERE 
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
                # print(results[0])
                # print(results[1])
                # print(results[2])
                # print(results[3])
                # print(results[4])
                student = Student(result[0], result[1], result[2], result[3], result[4])
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

    @classmethod
    def get_location_name_from_puid(cls, puid):
        str_puid = str(puid).strip()
        # build the sql statement
        stmt = f"""SELECT meal_plan_id FROM students WHERE puid
        =\'{str_puid}\'"""
        location_name = None

        try:
            # connection establishment
            params = config()
            conn = psycopg2.connect(**params)

            conn.autocommit = True
            cur = conn.cursor()

            cur.execute(stmt)
            meal_plan_id = cur.fetchone()[0]
            print(meal_plan_id)

            stmt2 = f"""SELECT location_id FROM students_plans
            WHERE meal_plan_id=\'{meal_plan_id}\'"""

            cur.execute(stmt2)
            location_id = cur.fetchone()[0]
            print(location_id)

            stmt3 = f"""SELECT location_name FROM locations
            WHERE location_id={location_id}"""

            cur.execute(stmt3)
            location_name = cur.fetchone()[0]
            print(location_name)

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

        return location_name

class Student:

    def __init__(self, puid, netid, name, mealplanid, isvalid):
        self._puid = puid
        self._netid = netid
        self._name = name
        self._mealplanid = mealplanid
        self._isvalid = isvalid
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
    # Students.get_friend_names(123456789)
    # print(Students.get_puid_from_name('Shayna'))
    # result = Students.search_students_by_name('a')
    # for item in result:
    #     print(item)

    print(Students.get_student_by_puid(920228016))
    print(Students.search_students_by_name('a'))
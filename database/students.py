from database import db_access
import psycopg2


# container class for students
class Students:

    # takes a puid as integer or string, puid should come from validated list of students (puid must already exist in db)
    @classmethod
    def get_student_by_puid(cls, puid):
        str_puid = str(puid).strip()
        stmt = f'''SELECT puid, netid, student_name, meal_plan_id, is_valid_for_meal_exchange FROM students WHERE 
                puid=\'{str_puid}\''''
        student_info = db_access.fetchone(stmt)
        student = Student(student_info[0], student_info[1], student_info[2], student_info[3], student_info[4])

        return student

    @classmethod
    def get_first_name_from_netid(cls, netid):
        str_netid = str(netid).strip()
        stmt = f'''SELECT student_name FROM students WHERE 
        netid=\'{str_netid}\''''
        name = db_access.fetch_first_val(stmt)

        if name is None:
            print('error: could not retrieve name')

        first_name = name.split(' ')[0]
        return first_name

    @classmethod
    def get_puid_from_netid(cls, netid):
        str_netid = str(netid).strip()
        stmt = f'''SELECT puid FROM students WHERE netid=\'{str_netid}\''''
        puid = db_access.fetch_first_val(stmt)

        return puid

    @classmethod
    def search_students_by_name(cls, name):
        str_name = str(name)
        stmt = f'''SELECT puid, netid, student_name, meal_plan_id, is_valid_for_meal_exchange FROM students WHERE 
        LOWER(student_name) LIKE LOWER(\'%{str_name}%\')'''
        students = []
        results = db_access.fetchall(stmt)
        for result in results:
            student = Student(result[0], result[1], result[2], result[3], result[4])
            students.append(student)

        return students

    # returns list of Student objects that are friends of the given puid
    @classmethod
    def get_friend_names(cls, puid):
        # build the sql statement
        stmt = f"""SELECT friend_puid FROM friends WHERE puid={puid}"""

        friend_data = []
        friend_puids = db_access.fetchall(stmt)

        for friend_puid in friend_puids:
            actual_puid = friend_puid[0]

            stmt2 = f"""SELECT student_name, meal_plan FROM 
            students WHERE puid=\'{actual_puid}\'"""
            row = db_access.fetchone(stmt2)

            student = Student(actual_puid, row[0], row[1])
            friend_data.append(student)

        return friend_data

    @classmethod
    def get_location_name_from_puid(cls, puid):
        str_puid = str(puid).strip()
        stmt = f"""SELECT meal_plan_id FROM students WHERE PUID
        =\'{str_puid}\'"""

        meal_plan_id = db_access.fetch_first_val(stmt)

        stmt2 = f"""SELECT location_id FROM student_plans
                    WHERE meal_plan_id=\'{meal_plan_id}\'"""

        location_id = db_access.fetch_first_val(stmt2)
        # print(location_id + "2")

        stmt3 = f"""SELECT location_name FROM locations
                    WHERE location_id=\'{location_id}\'"""

        location_name = db_access.fetch_first_val(stmt3)
        # print(location_name + "3")

        return location_name


class Student:

    def __init__(self, puid, netid, name, mealplanid, isvalid):
        self._puid = puid
        self._netid = netid
        self._name = name
        self._mealplanid = mealplanid
        self._isvalid = isvalid

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
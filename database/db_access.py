from config import config
import psycopg2


# opens and closes connection, returns list of rows retrieved by executing stmt
def fetchall(stmt,args=None):
    try:
        # connection establishment
        params = config()
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor()
        if args is not None:
            cur.execute(stmt % ('%' + args + '%'))
        else:
            cur.execute(stmt)
        
        return cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print('db_access.py: fetchall: ', error)
    finally:
        if conn is not None:
            cur.close()
            conn.close()


# opens and closes connection, returns first row retrieved by executing stmt
def fetchone(stmt):
    try:
        # connection establishment
        params = config()
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(stmt)
        return cur.fetchone()
    except (Exception, psycopg2.DatabaseError) as error:
        print('db_access.py: fetchone: ', error)
    finally:
        if conn is not None:
            cur.close()
            conn.close()


# opens and closes connection, returns first val in first row retrieved by executing stmt (ex. name)
def fetch_first_val(stmt):
    try:
        # connection establishment
        params = config()
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(stmt)
        result = cur.fetchone()
        if result is None:
            return None
        return result[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print('db_access.py: fetch_first_val: ', error)
    finally:
        if conn is not None:
            cur.close()
            conn.close()


# inserts data list into db using statement
def insert_data(stmt, data):
    try:
        # connection establishment
        params = config()
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(stmt, data)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print('db_access.py: insert_data: ', error)
    finally:
        if conn is not None:
            conn.close()
            print("insert data success")


# executes the given statement on the cursor
def execute_stmt(stmt):
    try:
        # connection establishment
        params = config()
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(stmt)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print('db_access.py: execute_stmt: ', error)
    finally:
        if conn is not None:
            conn.close()

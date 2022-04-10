from config import config
import psycopg2


# opens and closes connection, returns list of rows retrieved by executing stmt
def fetchall(stmt):
    try:
        # connection establishment
        params = config()
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(stmt)
        return cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            cur.close()
            conn.close()
            # print("fetch all success")


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
        print(error)
    finally:
        if conn is not None:
            cur.close()
            conn.close()
            # print("fetch one success")


# opens and closes connection, returns first val in first row retrieved by executing stmt (ex. name)
def fetch_first_val(stmt):
    try:
        # connection establishment
        params = config()
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(stmt)
        return cur.fetchone()[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            cur.close()
            conn.close()
            # print("fetch first val success")


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
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            cur.close()
            conn.close()
            print("insert data success")

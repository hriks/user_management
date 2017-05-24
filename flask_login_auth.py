# import Psycopg2 as pg

# --------------------------------------------------------------------


import psycopg2 as pg


# --------------------------------------------------------------------

# connection to database----------------------------------------------


def get_connection():
    try:
        conn = pg.connect(
            database='umnsntob',
            user='umnsntob',
            password='H7mI1xL-pv2MqfDsJNOG4SVDgxkRJJYq',
            host='stampy.db.elephantsql.com',
            port=5432)
        return conn
    except Exception as error:
        return error

# for authenticating ---------------------------------------------------
# Try except block is used for passing errors


def authenticate(username, password):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = """SELECT userid, password, role from "public"."user_rec" where userid='%s' and password='%s'"""  # noqa
        query = query % (username, password)
        cursor.execute(query)
        rows = cursor.fetchall()
        try:
            if (rows[0][0] == username) and (rows[0][1] == password):
                connection.close()
                return 1
            else:
                connection.close()
                return 0
        except Exception as error:
            return error
    except Exception as error:
        return error


# -------------------------------------------------------------------------
# Role verification -------------------------------------------------------
def role_authenticate(username, password):
    connection = get_connection()
    cursor = connection.cursor()
    query = """SELECT userid, password, role from "public"."user_rec" where userid='%s' and password='%s'"""  # noqa
    query = query % (username, password)
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows[0][2]


# -------------------------------------------------------------------------
# Search Box --------------------------------------------------------------
def searchbox(userid):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = """SELECT * FROM "public"."user_rec" WHERE userid LIKE '%s'"""
        query = query % ('%' + userid + '%')
        cursor.execute(query)
        rows = cursor.fetchall()
        connection.close()
        return rows
    except Exception as error:
        return error


# -------------------------------------------------------------------------
# User Blocked ------------------------------------------------------------
def blocked(username, password):
    connection = get_connection()
    cursor = connection.cursor()
    query = """SELECT userid, password, block from "public"."user_rec" where userid='%s' and password='%s'"""  # noqa
    query = query % (username, password)
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows[0][2]

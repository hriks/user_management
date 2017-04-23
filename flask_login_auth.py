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
    except Exception as e:
        raise e

# for authenticating ---------------------------------------------------
# Try except block is used for passing errors


def authenticate(username, password):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = """SELECT username, password from "public"."user"\
        where username='%s' and password='%s'"""
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
    except Exception as e:
        raise e
# -------------------------------------------------------------------------

# User data ---------------------------------------------------------------


def get_data(username, password):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = """SELECT * from "public"."user" where username='%s'\
        and password='%s'"""
        query = query % (username, password)
        cursor.execute(query)
        rows = cursor.fetchall()
        connection.close()
        return rows
    except Exception as e:
        raise e

# -------------------------------------------------------------------------
# Search Box --------------------------------------------------------------


def searchbox(name):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = """SELECT * from "public"."projects" where name='%s'"""
        query = query % (name)
        cursor.execute(query)
        rows = cursor.fetchall()
        print rows
        connection.close()
        return rows
    except Exception as e:
        raise e

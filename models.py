import psycopg2 as pg


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


def create_db():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            '''CREATE TABLE rec (
            ID  SERIAL PRIMARY KEY,
            USERID     TEXT   REFERENCES user_rec(USERID)  NOT Null,
            messages   TEXT
            );'''
        )
        connection.commit()
        connection.close()
    except Exception as error:
        return error


def post_messages(USER, MESSAGES):
    connection = get_connection()
    cursor = connection.cursor()
    print "cur is created"
    query = """INSERT INTO rec(USERID,MESSAGES) VALUES('%s', '%s');"""
    query = query % (
        USER, MESSAGES)
    print query
    cursor.execute(query)
    connection.commit()
    print "Message posted successfully"
    connection.close()


def process_create_user(USER, NAME, ROLE, EMAIL, PASSWORD):
    BLOCK = False
    connection = get_connection()
    cursor = connection.cursor()
    print "cur is created"
    query = """INSERT INTO user_rec(
    USERID,NAME,ROLE,BLOCK,PASSWORD,EMAIL
    ) VALUES('%s', '%s', '%s', '%s', '%s', '%s');"""
    query = query % (
        USER, NAME, ROLE, BLOCK, EMAIL, PASSWORD)
    print query
    cursor.execute(query)
    connection.commit()
    print "User created successfully"
    connection.close()


def create_user(USER, NAME, ROLE, EMAIL, PASSWORD):
    connection = get_connection()
    cursor = connection.cursor()
    query = """SELECT userid from user_rec where USERID='%s';"""
    query = query % (USER, )
    cursor.execute(query)
    rows = cursor.fetchall()
    print len(rows)
    try:
        if len(rows) == 0:
            process_create_user(USER, NAME, ROLE, EMAIL, PASSWORD)
            print "processed"
        else:
            print "FAILED"
            return 1
    except Exception as error:
        return error
    connection.close()


def message_show():
    connection = get_connection()
    cursor = connection.cursor()
    query = """SELECT * from rec;"""
    cursor.execute(query)
    rows = cursor.fetchall()
    print rows, len(rows)
    return rows
    connection.close()


def users():
    connection = get_connection()
    cursor = connection.cursor()
    query = """SELECT userid, name, email, role, block from user_rec;"""
    cursor.execute(query)
    rows = cursor.fetchall()
    print rows, len(rows)
    return rows
    connection.close()


def message_delete(id):
    connection = get_connection()
    cursor = connection.cursor()
    query = """DELETE FROM rec WHERE ID = %s;"""
    query = query % id
    print query
    cursor.execute(query)
    connection.commit()
    connection.close()
    return "Deleted"


def block(block, userid):
    connection = get_connection()
    cursor = connection.cursor()
    query = """UPDATE user_rec SET block = '%s' WHERE userid = '%s';"""
    query = query % (block, userid)
    print query
    cursor.execute(query)
    connection.commit()
    connection.close()
    return "DONE"

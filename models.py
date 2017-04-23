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
    query = """INSERT INTO LOGSS(USERID,MESSAGES) VALUES('%s', '%s');"""
    query = query % (
        USER, MESSAGES)
    print query
    cursor.execute(query)
    connection.commit()
    print "Message posted successfully"
    connection.close()


def create_user(USER, NAME, ROLE, EMAIL, PASSWORD):
    BLOCK = False
    connection = get_connection()
    cursor = connection.cursor()
    print "cur is created"
    query = """INSERT INTO user_rec(
    USER,NAME,ROLE,BLOCK,PASSWORD,EMAIL
    ) VALUES('%s', '%s', '%s', '%s', '%s');"""
    query = query % (
        USER, NAME, ROLE, BLOCK, EMAIL, PASSWORD)
    print query
    cursor.execute(query)
    connection.commit()
    print "User created successfully"
    connection.close()


def user_alreadyexits(USER, NAME, ROLE, EMAIL, PASSWORD):
    BLOCK = False
    connection = get_connection()
    cursor = connection.cursor()
    query = """SELECT USERID from  where USERID='%s';"""
    query = query % (USER, )
    cursor.execute(query)
    rows = cursor.fetchall()
    print rows
    try:
        if (len(rows) == 0):
            create_user(USER, NAME, ROLE, BLOCK, EMAIL, PASSWORD)
        else:
            return 1
    except Exception as error:
        return error
    connection.close()

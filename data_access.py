import os
import sqlite3
import csv
import random


def create_connection(db_file):
    """ Create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """
    Create a table from the create_table_sql statement

    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


def add_student(conn, student):
    """
    Add student into the students table

    :param conn:
    :param student:
    :return: student id
    """
    sql = '''
    INSERT INTO students(hw_id,first_name,last_name,email)
    VALUES(?,?,?,?);
    '''
    cur = conn.cursor()
    cur.execute(sql, student)
    conn.commit()
    return cur.lastrowid

def list_students(conn):
    sql = '''
    SELECT id, first_name, last_name from students;
    '''
    cur = conn.cursor()
    return cur.execute(sql)

def find_student_by_id(conn, _id):
    sql = 'SELECT * from students INNER JOIN hw ON students.id = hw.id WHERE students.id=?;'
    cur = conn.cursor()
    return next(cur.execute(sql, _id))


def init_db():
    database = 'data/main.db'

    if os.path.exists(database):
        print(f'Database {database} already exists')
        return
    else:
        print('Creating database...')

    sql_create_students_table = '''
    CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
	hw_id INTEGER NOT NULL UNIQUE,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	email TEXT NOT NULL
    );
    '''

    conn = create_connection(database)

    hwids = random.sample(range(100, 1000), 20)

    students = []

    if not os.path.exists('data/students.csv'):
        print('students.csv file not found')
        return

    with open('data/students.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        i = 0
        for row in csv_reader:
            a = row[0].split(maxsplit=1)
            first_name = a[0]
            last_name = a[1]
            email = row[1]

            students.append((hwids[i], first_name, last_name, email))
            i += 1

    students.sort(key=lambda x: x[2])

    with conn:
        create_table(conn, sql_create_students_table)
        print('Database successfully created\n')
        print('Adding student from data/students.csv:')
        for s in students:
            print(f'{s[1]} {s[2]}')
            add_student(conn, s)

def create_hw_table():
    database = 'data/main.db'

    sql_create_hw_table = '''
    CREATE TABLE IF NOT EXISTS hw (
    id INTEGER,
	hw_1 INTEGER,
	FOREIGN KEY(id) REFERENCES students(id)
    );
    '''

    conn = create_connection(database)

    with conn:
        create_table(conn, sql_create_hw_table)
        print('Table successfully created\n')

def add_hw():
    database = 'data/main.db'

    conn = create_connection(database)

    sql = "select * from hw;"
    with conn:
        new_hw_no = len(conn.cursor().execute(sql).description)
        sql_add_hw = f'ALTER TABLE hw ADD COLUMN hw_{new_hw_no}'
        conn.cursor().execute(sql_add_hw)

        print('Column added successfully')

def randomly_populate():
    database = 'data/main.db'

    conn = create_connection(database)
    tmp = ''
    for i in range(1,15):
        tmp += f'hw_{i},'
    tmp = tmp[:-1]
    sql = f'''
    INSERT INTO hw(id,{tmp})
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
    '''
    with conn:
        cur = conn.cursor()
        for i in range(1,6):
            a = [i]
            b = [random.randint(3,10) for _ in range(14)]
            cur.execute(sql, a+b)
            conn.commit()
    

# if __name__ == '__main__':
    # user_input = input('Do you want to add a new HW (y/n)? ')
    # if user_input == 'y':
    #     for i in range(13):
    #         add_hw()

    # user_input = input('Randomly populate HW results (y/n)? ')
    # if user_input == 'y':
    #     randomly_populate()

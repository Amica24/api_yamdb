import csv
import sqlite3


try:

    # Import csv and extract data
    with open('static/data/category.csv', 'r') as fin:
        dr = csv.DictReader(fin)
        csv_info = [(i['ID'], i['NAME'], i['SLUG']) for i in dr]
        print(csv_info)

    # Connect to SQLite
    sqliteConnection = sqlite3.connect('db.sqlite3')
    cursor = sqliteConnection.cursor()

    # Create student table
    cursor.execute(
        'create table category(id int, name varchar2(10), slug varchar2(10));'
    )

    # Insert data into table
    cursor.executemany(
        "insert into category (id, name, age) VALUES (?, ?, ?);", csv_info)

    # Show student table
    cursor.execute('select * from category;')

    # View result
    result = cursor.fetchall()
    print(result)

    # Commit work and close connection
    sqliteConnection.commit()
    cursor.close()

except sqlite3.Error as error:
    print('Error occured - ', error)

finally:
    if sqliteConnection:
        sqliteConnection.close()
        print('SQLite Connection closed')

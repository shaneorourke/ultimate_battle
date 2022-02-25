import sqlite3 as sql

conn = sql.connect('characters.db')
c = conn.cursor()

def amend_funds(value):
    c.execute(f'UPDATE bank SET balance = balance + {value}')
    conn.commit()

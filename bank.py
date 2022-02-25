import sqlite3 as sql

conn = sql.connect('characters.db')
c = conn.cursor()

def amend_funds(value):
    value = round(value,2)
    c.execute(f'UPDATE bank SET balance = balance + {value}')
    conn.commit()
    c.execute(f'UPDATE bank SET balance = ROUND(balance,2)')
    conn.commit()

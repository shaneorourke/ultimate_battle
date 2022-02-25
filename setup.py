import pandas as pd
import sqlite3 as sql
from random import randint

conn = sql.connect('characters.db')
c = conn.cursor()

filenames = ['./data/superheroes_stats.csv','./data/superheroes_info.csv','./data/superheroes_power_matrix.csv']

replace = ['(',')',',','./data/','csv','.']

def clean_up_sql_out(text):
    for s in replace:
        text = str(text).replace(s,'')
    return text

for filename in filenames:
    print(filename)
    filename_trim = clean_up_sql_out(filename)
    try:
        c.execute(f'select 1 from {filename_trim}')
        exists = c.fetchone()
    except:
        exists = 0
    exists = clean_up_sql_out(exists)
    print(f'Exists:{exists}')

    ## Create stats table from stats csv file - if it doesn't exist
    if exists == '0':
        print(f'Reading file:{filename}')
        stats = pd.read_csv(filename)
        print(f'Writing to table:{filename_trim}')
        stats.to_sql(f'{filename_trim}', conn)

def update_null_stats(column):
    c.execute(f'select max({column}) FROM superheroes_stats')
    max_value = c.fetchone()
    max_value = clean_up_sql_out(max_value)
    c.execute(f'select "index" from superheroes_stats WHERE {column} is null')
    nulls = c.fetchall()
    for id in nulls:
        index = clean_up_sql_out(id)
        rand_val = randint(0,int(max_value))
        if rand_val > 10:
            rand_val = rand_val / 10
        print(f'Setting ID:{index} {column} to {rand_val} MAX Val of {max_value}')
        c.execute(f'UPDATE superheroes_stats SET {column}={rand_val} WHERE "index" ={index}')

columns = ('Intelligence','Strength','Speed','Durability','Power','Combat','Total')
for column in columns:
    if column != 'Total':
        update_null_stats(column)
    if column == 'Total':
        c.execute('UPDATE superheroes_stats SET Total = Intelligence + Strength + Speed + Durability + Power + Combat')

c.execute('CREATE TABLE IF NOT EXISTS bank (balance int)')
c.execute('DELETE FROM bank')
c.execute('INSERT INTO bank VALUES (100)')

c.execute('CREATE TABLE IF NOT EXISTS records ("index" int, wins int, losses int, draws int)')
c.execute('DELETE FROM records')

c.execute('INSERT INTO records SELECT "index", 0, 0 ,0 from superheroes_stats')

conn.commit()
c.close()
import sqlite3 as sql
from random import randint

replace = ['(',')',',','./data/','csv','.']

def clean_up_sql_out(text):
    for s in replace:
        text = str(text).replace(s,'')
    return text

conn = sql.connect('characters.db')
c = conn.cursor()

def calc_odds(char_1,char_2):
    c.execute(f'select case when sum(wins) is null then 1 else sum(wins) end + case when sum(losses) is null then 1 else sum(losses) end / case when sum(wins) is null then 1 else sum(wins) end from records WHERE "index" in ({char_1},{char_2})')
    max_total = c.fetchone()
    max_total = clean_up_sql_out(max_total)
    print(f'ODDS:total wins:{max_total}')
    if max_total == None or max_total == 'None':
        max_total = 2

    c.execute(f'select wins from records WHERE "index" = {char_1}')
    wins = c.fetchone()
    wins = int(clean_up_sql_out(wins))
    print(f'ODDS:char 1 wins:{wins}')
    if wins == 0:
        wins = 1
    odds = int((int(max_total) / int(wins)))
    return odds


if __name__ == '__main__':
    print('poop')
import sqlite3 as sql
conn = sql.connect('characters.db')
c = conn.cursor()

def query(query):
    c.execute(query)
    result = c.fetchall()
    for row in result:
        print(row)

query_1 = "SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';"
query_2 = "PRAGMA table_info('superheroes_stats')"
query_3 = "PRAGMA table_info('superheroes_info')"
query_4 = "PRAGMA table_info('superheroes_power_matrix')"
#query(query_2)

c.execute("""SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';""")
out = c.fetchall()
#print(out)

c.execute("SELECT * FROM records where wins >= 2 OR losses >= 2")
out = c.fetchall()
#print(out)


c.execute("SELECT * FROM bank")
out = c.fetchall()
print(out)


c.execute("SELECT * FROM superheroes_stats st INNER JOIN superheroes_info inf ON st.'name' = inf.'name' WHERE st.name = 'Ultron' LIMIT 1")
out = c.fetchall()
#print(out)

c.execute("SELECT * FROM superheroes_stats st WHERE st.name = 'Vanisher'")
out = c.fetchall()
#print(out)
c.execute("SELECT * FROM superheroes_info st WHERE st.name = 'Ultron'")
out = c.fetchall()
#print(out)


def char_selector():
    index = 87
    c.execute(f'SELECT st.*, inf.status, inf.gender, inf.race, inf.publisher FROM superheroes_stats st INNER JOIN superheroes_info inf ON st.name = inf.name WHERE st."index"={index} LIMIT 1')
    result = c.fetchone()
    if result == None:
        c.execute(f'SELECT st.*, inf.status, inf.gender, inf.race, inf.publisher FROM superheroes_stats st LEFT JOIN superheroes_info inf ON REPLACE(REPLACE(st.name," ",""),"I","") = REPLACE(inf.name," ","") WHERE st."index"={index} LIMIT 1')
        result = c.fetchone()
    return result

c.execute('select sum(payout) from bets')
out = c.fetchall()
for row in out:
    print(row)
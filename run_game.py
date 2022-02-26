import battle as b
import sqlite3 as sql

conn = sql.connect('characters.db')
c = conn.cursor()

replace = ['(',')',',','./data/','csv','.']
replace_number = ['(',')',',']

def clean_up_sql_out(text,isnumber):
    if isnumber == 1:
        for s in replace_number:
            text = str(text).replace(s,'')      
    else:
        for s in replace:
            text = str(text).replace(s,'')
    return text

c.execute(f'SELECT max(balance) FROM bank_history')
highscore = clean_up_sql_out(c.fetchone(),1)

c.execute(f'SELECT balance FROM bank')
current_balance = clean_up_sql_out(c.fetchone(),1)

welcome = f"""#############################################################
#                                                           #
#            WELCOME TO THE BATTLE!!                        #
#            The game is simple, bet on                     # 
#            which superhero will win (or lose)             #
#            SEE IF YOU CAN BEAT YOUR TOP BALANCE           #
#                                                           #
#############################################################

HIGH SCORE:£{highscore}
CURRENT BALANCE:£{current_balance}
"""
print(welcome)
inplay = input('Press Enter To Begin')

while inplay == '':
    b.main()
    inplay = input('Press Enter To Continue - Any Key To Quit')
    if inplay != '':
        print('QUITING')
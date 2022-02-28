import battle as b
import sqlite3 as sql
from rich.console import Console
from rich.theme import Theme
from rich.markdown import Markdown

customer_theme = Theme({'info':"bold green italic",'vs':"bold blue",'warn':"red underline",'win':"blue bold",'draw':"yellow",'lose':"red bold",'winlabel':"blue bold blink",'drawlabel':"yellow blink",'loselabel':"red bold blink"})
console = Console(theme=customer_theme)
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

welcome_old = f"""#############################################################
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

welcome = """
# **WELCOME TO THE BATTLE!!**
> ***The game is simple, bet on which superhero will win (or lose) SEE IF YOU CAN BEAT YOUR TOP BALANCE***
"""
md = Markdown(welcome)
console.print(md)
inplay = console.input('Press Enter To Begin: Enter "1" for Stats Light Mode:')
if inplay == '1':
    light_mode = 1
    inplay = ''
else:
    light_mode = 0

while inplay == '':
    b.main(light_mode)
    inplay = console.input('Press Enter To Continue - Any Key To Quit')
    if inplay != '':
        console.print('QUITING')
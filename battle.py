import sqlite3 as sql
from random import randint
from xmlrpc.client import boolean
import pandas as pd
import bank as ba
import odds as od


conn = sql.connect('characters.db')
c = conn.cursor()
c.execute(f'SELECT max("index") FROM superheroes_stats')
max_index = c.fetchone()

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

def round_float(value):
    value = round(float(value),2)
    return value

max_index = int(clean_up_sql_out(max_index,0))

def cls():
    print('\n'*50)

def list_2_dict_convert(a):
    it = iter(a)
    res_dct = dict(zip(it, it))
    return res_dct
         
def char_selector(max_index):
    index = randint(1,max_index)
    c.execute(f'SELECT st.*, inf.status, inf.gender, inf.race, inf.publisher FROM superheroes_stats st INNER JOIN superheroes_info inf ON st.name = inf.name WHERE st."index"={index} LIMIT 1')
    result = c.fetchone()
    if result == None:
        c.execute(f'SELECT st.*, inf.status, inf.gender, inf.race, inf.publisher FROM superheroes_stats st LEFT JOIN superheroes_info inf ON REPLACE(REPLACE(st.name," ",""),"I","") = REPLACE(inf.name," ","") WHERE st."index"={index} LIMIT 1')
        result = c.fetchone()
    return result
    
def bet_record(char_1, char_2, winner, bet_amount, payout, odds, balance_before, balance_after):
    c.execute(f'INSERT INTO bets (char_1, char_2, winner, bet_amount, payout, odds, balance_before, balance_after) VALUES ("{char_1}", "{char_2}", "{winner}", {bet_amount}, {payout}, {odds}, {balance_before}, {balance_after})')
    conn.commit()


def main(light_mode):
    cls()
    char_1 = char_selector(max_index)
    lst = ['index', char_1[0], 'name', char_1[1], 'alignment', char_1[2], 'intelligence',char_1[3],'strength',char_1[4],'speed',char_1[5],'durability',char_1[6],'power',char_1[7],'combat',char_1[8],'total',char_1[9], 'status',char_1[10], 'gender',char_1[11], 'race',char_1[12], 'publisher',char_1[13]]
    char_1 = list_2_dict_convert(lst)
    char_df = pd.DataFrame.from_records(char_1,index=[0],columns=['index','name','alignment','intelligence','strength','speed','durability','power','combat','total','status','gender','race','publisher'])

    char_2 = char_selector(max_index)
    lst = ['index', char_2[0], 'name', char_2[1], 'alignment', char_2[2], 'intelligence',char_2[3],'strength',char_2[4],'speed',char_2[5],'durability',char_2[6],'power',char_2[7],'combat',char_2[8],'total',char_2[9], 'status',char_2[10], 'gender',char_2[11], 'race',char_2[12], 'publisher',char_2[13]]
    char_2 = list_2_dict_convert(lst)
    char_df = char_df.append(char_2,ignore_index=True)

    def print_stats(iloc):
        print('Name:',char_df['name'].iloc[iloc])
        print('Alignment:',char_df['alignment'].iloc[iloc])
        print('Status:',char_df['status'].iloc[iloc])
        print('Gender:',char_df['gender'].iloc[iloc])
        print('Race:',char_df['race'].iloc[iloc])
        print('Publisher:',char_df['publisher'].iloc[iloc])

        print('Intelligence:',char_df['intelligence'].iloc[iloc])
        print('Strength:',char_df['strength'].iloc[iloc])
        print('Speed:',char_df['speed'].iloc[iloc])
        print('Durability:',char_df['durability'].iloc[iloc])
        print('Power:',char_df['power'].iloc[iloc])
        print('Combat:',char_df['combat'].iloc[iloc])
        print('Total:',round(char_df['total'].iloc[iloc],2))

    def print_stats_light(iloc):
        print('Name:',char_df['name'].iloc[iloc])
        print('Total:',round(char_df['total'].iloc[iloc],2))

    print()
    if light_mode != True:
        print_stats(0)
    else:
        print_stats_light(0)
    print()
    print('VERSUS')
    print()
    name2 = char_df['name'].iloc[1]
    print('name:',name2)
    if light_mode != True:
        print('alignment:',char_df['alignment'].iloc[1])
        print('Status:',char_df['status'].iloc[1])
        print('Gender:',char_df['gender'].iloc[1])
        print('Race:',char_df['race'].iloc[1])
        print('Publisher:',char_df['publisher'].iloc[1])
    print()
    name1 = char_df['name'].iloc[0]
    win_or_lose = input(f'Will {name1} Win? (yes, y, 1 OR no, n, 0):')
    if win_or_lose.lower() in ('yes',str(1),'y'):
        win_or_lose = True
    else:
        win_or_lose = False
    c.execute('SELECT balance FROM bank')
    balance = c.fetchone()
    balance = clean_up_sql_out(balance,1)
    balance_before = balance
    if balance == '0':
        print('You\'re out of funds, here\'s £10 to help you build that balance again')
        ba.amend_funds(10)
        balance = 10

    if win_or_lose:
        odds = od.calc_odds(char_df['index'].iloc[0],char_df['index'].iloc[1])
    else:
        odds = od.calc_odds(char_df['index'].iloc[1],char_df['index'].iloc[0])

    print(f'Odds:{odds}')
    print('Quick bets: a=10% b=25% c=50% d=75% z=100%')
    bet_amount = input(f'Balance:£{balance} Bet Amount:£')
    if bet_amount == '' or bet_amount == None:
        bet_amount_default = 1
    if bet_amount.lower() in ('a','b','c','d','z'):
        if bet_amount.lower() == 'a':
            bet_amount_default = round_float(float(balance)*0.1)
        if bet_amount.lower() == 'b':
            bet_amount_default = round_float(float(balance)*0.25)
        if bet_amount.lower() == 'c':
            bet_amount_default = round_float(float(balance)*0.5)
        if bet_amount.lower() == 'd':
            bet_amount_default = round_float(float(balance)*0.75)
        if bet_amount.lower() == 'z':
            bet_amount_default = round_float(float(balance))
    else:
        bet_amount_default = bet_amount
    bet_amount = round_float(bet_amount_default)
    if round_float(bet_amount) > round_float(float(balance)):
        print(f'You havent got the funds for this bet - Setting bet to £{balance}')
        bet_amount = round_float(balance)
        wait = input('Press Enter to Continue')

    cls()

    if char_df['total'].iloc[0] > char_df['total'].iloc[1] and win_or_lose:
        print('##################### WIN #####################')
        winner = char_df['index'].iloc[0]
        loser = char_df['index'].iloc[1]
        c.execute(f'UPDATE records SET wins = wins+1 WHERE "index" = {winner}')
        conn.commit()
        c.execute(f'UPDATE records SET losses = losses+1 WHERE "index" = {loser}')
        conn.commit()
        amount = round_float(bet_amount*odds)
        ba.amend_funds(amount)

    elif char_df['total'].iloc[0] < char_df['total'].iloc[1] and win_or_lose == False:
        print('##################### WIN #####################')
        winner = char_df['index'].iloc[1]
        loser = char_df['index'].iloc[0]

        c.execute(f'UPDATE records SET wins = wins+1 WHERE "index" = {winner}')
        conn.commit()
        c.execute(f'UPDATE records SET losses = losses+1 WHERE "index" = {loser}')
        conn.commit()
        amount = round_float(bet_amount*odds)
        ba.amend_funds(amount)

    elif char_df['total'].iloc[0] == char_df['total'].iloc[1]:
        print('##################### Draw #####################')
        draw1 = char_df['index'].iloc[0]
        draw2 = char_df['index'].iloc[1]
        c.execute(f'UPDATE records SET draws = draws+1 WHERE "index" in({draw1},{draw2})')
        amount = 0
        conn.commit()
    else:
        print('##################### LOSE #####################')
        if win_or_lose == True:
            winner = char_df['index'].iloc[0]
            loser = char_df['index'].iloc[1]
        else:
            winner = char_df['index'].iloc[1]
            loser = char_df['index'].iloc[0]

        amount = round_float(bet_amount*-1)
        ba.amend_funds(amount)
    conn.commit()
    print(f'winner:{winner} loser:{loser}')
    if light_mode != True:
        print_stats(0)
    else:
        print_stats_light(0)
    print()
    if light_mode != True:
        print_stats(1)
    else:
        print_stats_light(1)

    print()
    print(f'Bet Amount£:{bet_amount}')
    print(f'Payout:£{amount}')
    c.execute('SELECT balance FROM bank')
    balance = c.fetchone()
    balance = clean_up_sql_out(balance,1)
    print()
    print(f'New Balance:{balance}')
    bet_record(char_1, char_2, winner, bet_amount, amount, odds, balance_before, balance)
    ba.audit_bank()

if __name__ == '__main__':
    print('poop')
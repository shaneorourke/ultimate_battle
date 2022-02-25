import sqlite3 as sql
from random import randint
import pandas as pd
import bank as ba
import odds as od

conn = sql.connect('characters.db')
c = conn.cursor()
c.execute(f'SELECT max("index") FROM superheroes_stats')
max_index = c.fetchone()

replace = ['(',')',',','./data/','csv','.']

def clean_up_sql_out(text):
    for s in replace:
        text = str(text).replace(s,'')
    return text

max_index = int(clean_up_sql_out(max_index))

def cls():
    print('\n'*50)

def list_2_dict_convert(a):
    it = iter(a)
    res_dct = dict(zip(it, it))
    return res_dct
         
def char_selector(max_index):
    index = randint(1,max_index)
    c.execute(f'SELECT * FROM superheroes_stats WHERE "index"={index}')
    result = c.fetchone()
    return result

    
def main():
    cls()
    char_1 = char_selector(max_index)
    lst = ['index', char_1[0], 'name', char_1[1], 'alignment', char_1[2], 'intelligence',char_1[3],'strength',char_1[4],'speed',char_1[5],'durability',char_1[6],'power',char_1[7],'combat',char_1[8],'total',char_1[9]]
    char_1 = list_2_dict_convert(lst)
    char_df = pd.DataFrame.from_records(char_1,index=[0],columns=['index','name','alignment','intelligence','strength','speed','durability','power','combat','total'])

    char_2 = char_selector(max_index)
    lst = ['index', char_2[0], 'name', char_2[1], 'alignment', char_2[2], 'intelligence',char_2[3],'strength',char_2[4],'speed',char_2[5],'durability',char_2[6],'power',char_2[7],'combat',char_2[8],'total',char_2[9]]
    char_2 = list_2_dict_convert(lst)
    char_df = char_df.append(char_2,ignore_index=True)

    def print_stats(iloc):
        print('name:',char_df['name'].iloc[iloc])
        print('alignment:',char_df['alignment'].iloc[iloc])
        print('intelligence:',char_df['intelligence'].iloc[iloc])
        print('strength:',char_df['strength'].iloc[iloc])
        print('speed:',char_df['speed'].iloc[iloc])
        print('durability:',char_df['durability'].iloc[iloc])
        print('power:',char_df['power'].iloc[iloc])
        print('combat:',char_df['combat'].iloc[iloc])
        print('total:',char_df['total'].iloc[iloc])

    print()
    print_stats(0)
    print()
    print('VERSUS')
    print()
    name2 = char_df['name'].iloc[1]
    print('name:',name2)
    print('alignment:',char_df['alignment'].iloc[1])
    print()
    name1 = char_df['name'].iloc[0]
    win_or_lose = input(f'Will {name1} Win?')
    if win_or_lose.lower() in ('yes',str(1),'y'):
        win_or_lose = True
    else:
        win_or_lose = False
    c.execute('SELECT balance FROM bank')
    balance = c.fetchone()
    balance = clean_up_sql_out(balance)
    if balance == '0':
        print('You\'re out of funds, here\'s £10 to help you build that balance again')
        ba.amend_funds(10)
        balance = 10

    odds = od.calc_odds(char_df['index'].iloc[0],char_df['index'].iloc[1])
    print(f'Odds:{odds}/1')
    print('Quick bets: a=10% b=25% c=50% d=75%')
    bet_amount = input(f'Balance:£{balance} Bet Amount:£')
    if bet_amount.lower() in ('a','b','c','d'):
        if bet_amount.lower() == 'a':
            bet_amount_default = int(balance)*0.1
        if bet_amount.lower() == 'b':
            bet_amount_default = int(balance)*0.25
        if bet_amount.lower() == 'c':
            bet_amount_default = int(balance)*0.5
        if bet_amount.lower() == 'd':
            bet_amount_default = int(balance)*0.75
    else:
        bet_amount_default = bet_amount
    bet_amount = int(bet_amount_default)
    if int(bet_amount) > int(balance):
        print(f'You havent got the funds for this bet - Setting bet to £{balance}')
        bet_amount = int(balance)
        wait = input('Press Enter to Continue')

    cls()
    
    if char_df['total'].iloc[0] > char_df['total'].iloc[1] and win_or_lose:
        print('##################### WIN #####################')
        winner = char_df['index'].iloc[0]
        loser = char_df['index'].iloc[1]
        print(f'winner:{winner} loser:{loser}')
        c.execute(f'UPDATE records SET wins = wins+1 WHERE "index" = {winner}')
        conn.commit()
        c.execute(f'UPDATE records SET losses = losses+1 WHERE "index" = {loser}')
        conn.commit()
        amount = bet_amount*odds
        ba.amend_funds(amount)

    elif char_df['total'].iloc[0] < char_df['total'].iloc[1] and win_or_lose == False:
        print('##################### WIN #####################')
        winner = char_df['index'].iloc[1]
        loser = char_df['index'].iloc[0]
        print(f'winner:{winner} loser:{loser}')
        c.execute(f'UPDATE records SET wins = wins+1 WHERE "index" = {winner}')
        conn.commit()
        c.execute(f'UPDATE records SET losses = losses+1 WHERE "index" = {loser}')
        conn.commit()
        amount = bet_amount*odds
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
        amount = bet_amount*-1
        ba.amend_funds(amount)
    conn.commit()
    print_stats(0)
    print()
    print_stats(1)

    print()
    print(f'Bet Amount£:{bet_amount}')
    print(f'Payout:£{amount}')
    c.execute('SELECT balance FROM bank')
    balance = c.fetchone()
    balance = clean_up_sql_out(balance)
    print()
    print(f'New Balance:{balance}')

if __name__ == '__main__':
    print('poop')
import battle as b

welcome = """#####################################################
#                                                   #
#            WELCOME TO THE BATTLE!!                #
#            The game is simple, bet on             # 
#            which superhero will win (or lose)     #
#            SEE IF YOU CAN BEAT YOUR TOP BALANCE   #
#                                                   #
#####################################################
"""
print(welcome)
inplay = input('Press Enter To Begin')

while inplay == '':
    b.main()
    inplay = input('Press Enter To Continue - Any Key To Quit')
    if inplay != '':
        print('QUITING')
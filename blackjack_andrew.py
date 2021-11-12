'''
Blackjack game for Udemy python intro course
Written by AN on 2021-11-11
pylint score = 6.35 / 10
'''

import blackjack_classes

def get_bet(cash):
    '''ask for bet, validate answer, return integer'''
    is_int = False
    enough_cash = False
    
    while not is_int or not enough_cash:
        
        try:
            response = int(input(f"You have ${cash}. How much would you like to bet? "))
        except:
            print("Not an int! Please try again.")
            is_int = False
            continue
        else:
            is_int = True
                
        enough_cash = response <= cash
        if not enough_cash:
            print("Bet exceeds amount you have")
   
    return response

def want_to_keep_playing():
    ''' ask if want to keep playing, validate answer, return true / false'''
    response = ''
    
    while True:
        response = input("Want to play another round? (Y/N): ")
        if response.upper() not in ['Y','N']:
            print("Not an acceptable input, please try again.")
        else:
            break
            
    return (response.upper() == "Y")

def intro_questions():
    ''' Asks user questions and returns tuple with player name, # decks to use'''
    name = input("Welcome to S17 BlackJack! Everyone starts with $100. Please enter your name: ")
    is_int = False
    max_10 = False
    
    while not is_int or not max_10:
        try:
            decks = int(input("How many card decks should we play with? ")) 
        except:
            print("Not an int! Please try again.")
            is_int = False
            continue
        else:
            is_int = True
        
        max_10 = (decks <= 10 and decks > 0)
        if not max_10:
            print("Please re-enter a number between 1 and 10 for the number of decks.")
    
    return (name,decks)

def play_blackjack():
    game_on = True
    round_on = True
    decks = []
    player_bet = 0
    
    # input section: prompt for name, # decks to use
    player_name,num_decks = intro_questions()
    
    for _ in range(0,num_decks):
        a_deck = blackjack_classes.Deck()
        decks.append(a_deck)
    
    # initialize players
    player_one = blackjack_classes.Player(player_name,100)
    dealer = blackjack_classes.Dealer()
    
    the_table = blackjack_classes.Table(decks)
    
    while game_on:
        the_table.display(player_one.hand,dealer.hand,player_bet,player_one.cash)
        
        # ask how much you would like to bet
        player_bet = get_bet(player_one.cash)
        
        # deal cards: 2 to player, 1 to dealer
        player_one.take_cards(the_table.deal(2))
        dealer.take_cards(the_table.deal(1))
        
        round_on = True
        
        while round_on:
            the_table.display(player_one.hand,dealer.hand,player_bet,player_one.cash)

            # player's turn first. They either lose the round
            # or the round continues
            (victory_status,player_one_score) = player_one.take_turn(the_table,dealer.hand,player_bet)
            if  victory_status == 'PLAYER LOSES':
                break
            # dealer's turn
            victory_status = dealer.take_turn(player_one_score,the_table)
            round_on = False
        
        # settle up money
        if victory_status == 'PLAYER LOSES':
            player_one.lose_money(player_bet)
        elif victory_status == "TIE":
            player_one.lose_money(0)
        else:
            player_one.win_money(player_bet)
        
        # display table and announce winner
        the_table.display(player_one.hand,dealer.hand,player_bet,player_one.cash)
        if victory_status == "PLAYER LOSES":
            print(f"Sorry {player_one.name}, you lost ${player_bet}")
        elif victory_status == "TIE":
            print(f"Tie game! {player_one.name}, you get your money back.")
        else:
            print(f"Congratulations {player_one.name} on winning ${player_bet}")
        
        # settle up cards
        the_table.discard_cards(player_one.clear_hand())
        the_table.discard_cards(dealer.clear_hand())
        
        if player_one.cash == 0:
            print(f"{player_one.name} is out of money! Game over!")
            break
        
        # want to keep playing?
        game_on = want_to_keep_playing()
    
    print(f"Thanks for playing! {player_one.name} walks away with ${str(player_one.cash)}")

if __name__ == "__main__":
    play_blackjack()

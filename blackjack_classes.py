'''
All classes for blackjack game stored within this module
pylint score = 5.76
'''
import random
import os

VALUE_LOOKUP = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10,'A':11}
LIST_OF_RANKS = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
LIST_OF_SUITS = ['Spades','Hearts','Clubs','Diamonds']

def clear_output():
    # for Windows:
    if os.name == 'nt':
        _ = os.system('cls')
    # for mac and linux, os.name is "posix"
    else:
        _ = os.system('clear')

class Card():
    ''' Card class represents a single card with properties of suit, rank, value '''        
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = VALUE_LOOKUP[rank]
    
    def __str__(self):
        return f"{self.rank:>2} of {self.suit:10}"

class Deck():
    ''' Deck class represents a standard 52-card deck of playing cards. It can be shuffled '''
    def __init__(self):
        self.card_list = []        
        # create 52 card deck with all values, all in order
        for suit in LIST_OF_SUITS:
            for rank in LIST_OF_RANKS:
                self.card_list.append(Card(suit,rank))
        
    def shuffle(self):
        random.shuffle(self.card_list)
        
    def __str__(self):
        str1 = ''
        for item in self.card_list:
            str1 += str(item)
            str1 += '\n'
        return str1

class Table():
    ''' Table class represents the play area. It includes the pickup card pile,
        discard pile, the player's money and bet, and the hands'''
    def __init__(self,decks):
        self.to_deal_list = []
        for index,_ in enumerate(decks):
            for card in decks[index].card_list:
                self.to_deal_list.append(card)
            
        random.shuffle(self.to_deal_list)
        
        self.discarded_list = []
    
    def display(self,player_one_hand,dealer_hand,bet,cash):
        # for now, lame visual representation:
        clear_output()
        print(f"Player cash: {cash}")
        print(f"Player's current bet: {bet}")
        print(f"Cards in pickup pile: {len(self.to_deal_list)}")
        print(f"Cards in discard pile: {len(self.discarded_list)}")
        print(f"Dealer's hand: total {dealer_hand.calculate_sum()}")
        print(dealer_hand)
        print(f"Player's hand: total {player_one_hand.calculate_sum()}")
        print(player_one_hand)
    
    def deal(self,num_cards):
        # pop num_cards from to_deal_list and return list of cards
        self.deal_list = []
        for _ in range(0,num_cards):
            if len(self.to_deal_list) > 0:
                self.deal_list.append(self.to_deal_list.pop(0))
            else:
                self.reshuffle_discard()
                self.deal_list.append(self.to_deal_list.pop(0))
        
        return self.deal_list
    
    def reshuffle_discard(self):
        # only ever called when main deal pile is empty.
        # function moves everything from discard pile into main deal pile
        # and shuffles the main deal pile again
        self.to_deal_list = self.discarded_list
        self.discarded_list = []
        random.shuffle(self.to_deal_list)
    
    def discard_cards(self,card_list):
        # takes in list of cards that came from player's hand, puts those cards into discarded list
        for card in card_list:
            self.discarded_list.append(card)

class Player():
    ''' Player class represents blackjack player or dealer, they have money,
        a hand, they can take a turn '''    
    def __init__(self,name='Dealer',initial_money='0'):
        self.name = name
        self.cash = initial_money
        self.hand = Hand()        
        
    def take_cards(self,card_list):
        new_sum = 0
        for card in card_list:
            new_sum = self.hand.add(card)
        return new_sum
    
    def win_money(self,money):
        self.cash += money
    
    def lose_money(self,money):
        self.cash -= money
    
    def clear_hand(self):
        return self.hand.clear_hand()
    
    def prompt_move(self):
        while True:
            
            self.response = input(f"Current sum is {self.hand.calculate_sum()}. What will you do (Hit or Stay)? ")
            if self.response.lower() not in ['hit','stay']:
                print("Please enter a valid input")
            else:
                if self.response.lower() == 'hit':
                    self.response = 'Hit'
                else:
                    self.response = 'Stay'
                break
        return self.response
    
    def take_turn(self,table,dealer_hand,player_bet):
        # returns (victory status, score)
        # victory status: either "PLAYER LOSES" or "NOT FINISHED"
        # score: sum of their hand
        while True:
            self.response = self.prompt_move()
            if self.response == 'Stay':
                return ("NOT FINISHED", self.hand.calculate_sum())
            else:
                # player entered "hit"
                if self.take_cards(table.deal(1)) > 21:
                    return ("PLAYER LOSES", self.hand.calculate_sum())
                else:
                    table.display(self.hand,dealer_hand,player_bet,self.cash)
                    continue

class Dealer(Player):
    ''' Dealer class inherits from player class. Dealer uses methods take_cards
        and clear_hand and __init__ but doesn't need any of the other methods '''
    
    def take_turn(self,score,table):
        # returns victory status: either "PLAYER LOSES" or "PLAYER WINS" or "TIE"
        # here is where logic will go for different dealer rules: soft/hard 17 etc.
        # for now making logic be if dealer is < player, dealer continues playing
        while self.hand.calculate_sum() < score and self.hand.calculate_sum() < 17:
            # Hit
            self.take_cards(table.deal(1))
        
        if self.hand.calculate_sum() > 21 or self.hand.calculate_sum() < score:
            return "PLAYER WINS"
        if self.hand.calculate_sum() > score:
            return "PLAYER LOSES"
        return "TIE"

class Hand():
    ''' Class representing player's hand. We can calculate its sum,
    add cards to it, discard the hand when we're done'''    
    def __init__(self):
        self.card_list = []
        self.sum = 0
        self.ace_positions = []
        
    def __str__(self):
        self.output_string = ''
        for card in self.card_list:
            self.output_string += str(card)
        return self.output_string
    
    def add(self,card):
        self.card_list.append(card)
        return self.calculate_sum()
    
    def calculate_sum(self):
        self.sum = 0
        self.ace_positions.clear()
        for index, card in enumerate(self.card_list):
            if card.rank == 'A':
                self.ace_positions.append(index)
            self.sum += card.value
            while len(self.ace_positions) > 0 and self.sum > 21:
                self.sum -= 10
                self.ace_positions.pop(0)
                
        return self.sum         
    
    def clear_hand(self):
        ''' returns list of cards and clears card_list and sum '''
        self.output_list = []
        for card in self.card_list:
            self.output_list.append(card)
        self.card_list.clear()
        self.ace_positions.clear()
        self.sum = 0
        
        return self.output_list

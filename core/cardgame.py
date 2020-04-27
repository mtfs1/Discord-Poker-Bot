'''
A pretty simple module made to help future card games
in python programmes

There are three main classes, representing the objects
of cards, decks and players

The module doesn't implement any kind of game rules, so
it can be used in a diversity of diferent programmes that
implement diferent types of deck games
'''

import random

RANKS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
SUITS = ('Diamonds', 'Spades', 'Hearts', 'Clubs')

# 
# A class representing a single card of a default 52 cards deck
# 
class Card:
    def __init__(self, rank, suit:str):
        if rank in RANKS:
            if suit in SUITS:
                self.rank = rank
                self.suit = suit
                self.slug = (suit[0], rank)
            else:
                raise Exception('Invalid suit')
        else:
            raise Exception('Invalid rank')

    # An prettier form of debugging the card object by print()
    def __str__(self):
        if self.rank == 1:
            rank = 'A'
        elif self.rank == 11:
            rank = 'J'
        elif self.rank == 12:
            rank = 'Q'
        elif self.rank == 13:
            rank = 'K'
        elif self.rank == 14:
            rank = 'A'
        return f'{self.rank} of {self.suit}'

    # returns the name of the card
    def return_card(self):
        if self.rank in (11, 12, 13, 14):
            rank_to_letter = {11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace'}
            return f'{rank_to_letter[self.rank]} of {self.suit}'
        return f'{self.rank} of {self.suit}'

    # returns the rank simbol of the card, either a number or a letter
    def return_rank_simbol(self):
        if self.rank in (11, 12, 13, 14):
            rank_to_letter = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
            return rank_to_letter[self.rank]
        return self.rank

    # prints the name of the card
    def show_card(self):
        if self.rank in (11, 12, 13, 14):
            rank_to_letter = {11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace'}
            return f'{rank_to_letter[self.rank]} of {self.suit}'
        print(f'{self.rank} of {self.suit}')

# 
# A class representing a default deck, with 52 cards
# 
class Deck:
    def __init__(self):
        self.cards = []
        for t in SUITS:
            for v in RANKS:
                self.cards.append(Card(v, t))
    
    # returns the card in the top of the deck
    def withdraw_card(self):
        return self.cards.pop()

    # put a card in the top of the deck
    def put_card(self, card:Card):
        self.cards.append(card)

    # shuffles the entire deck, randomize the order of the cards
    def shuffle(self):
        random.shuffle(self.cards)

    # prints the cards of the deck in the order that they are shuffled
    def show(self):
        for c in self.cards:
            c.show_card()
    
    # prints the number of cards in the deck in that moment
    def show_deck_length(self):
        print(len(self.cards))
    
    # returns the number of cards in the deck in that moment
    def return_deck_length(self):
        return len(self.cards)

    # returns a list with the slug of all cards in the deck in that moment
    def return_slug(self):
        slug_list = []
        for c in self.cards:
            slug_list.append(c.slug)
        return slug_list
    
# 
# A class representing a player, with a hand of cards withdarawn from a deck
# 
class Player:

    number_of_instances = 0

    def __init__(self, name:str, points:int = 0, money = 0):
        self.name = name
        self.hand = []
        self.points = points
        self.money = money

        self.id = Player.number_of_instances
        Player.number_of_instances += 1

    # the player withdraw the card on the top of the deck and add it to your hand
    def withdraw_card(self, deck:Deck):
        self.hand.append(deck.withdraw_card())

    # the player discard one card of your hand and put it on the top of the deck
    def discard_card(self, index:int, deck:Deck):
        if index < 0:
            raise Exception('Negative value for index is not allowed')
        if index >= len(self.hand):
            raise Exception('Index out of bounds')
        deck.put_card(self.hand[index])
        del self.hand[index]

    # the player discard all your cards and put them on the top of the deck
    def discard_all_cards(self, deck:Deck):
        for c in self.hand:
            deck.put_card(c)
        self.hand = []

    # prints all the cards from the player's hand
    def show_hand(self):
        for c in self.hand:
            c.show_card()
    
    # prints the number of cards in the player's hand
    def show_hand_length(self):
        print(len(self.hand))
    
    # returns the number of cards in the player's hand
    def return_hand_length(self):
        return len(self.hand)

    # returns a list of slugs of the cards in the player's hand
    def return_slug(self):
        slug_list = []
        for c in self.hand:
            slug_list.append(c.slug)
        return slug_list

    # subtracts money if the amount given fit in the real quantity of money of the player 
    def subtract_money(self, amount):
        if amount > self.money:
            amount_subtracted = amount - self.money
            self.money = 0
            return amount_subtracted
        else:
            self.money -= amount
            return amount
    
    # subtracts points if the amount given fit in the real quantity of points of the player
    def subtract_points(self, amount):
        if amount > self.points:
            raise Exception("Trying to take more points than player has")
        else:
            self.points -= amount
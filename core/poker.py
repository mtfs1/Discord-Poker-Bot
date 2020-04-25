import core.cardgame as cardgame
# import cardgame as cardgame
import pprint

def equal(self, other):
    return (self.rank == other.rank)

def not_equal(self, other):
    return (self.rank != other.rank)

def lower_than(self, other):
    return (self.rank < other.rank)

def greater_than(self, other):
    return (self.rank > other.rank)

def lower_or_equal_to(self, other):
    return (self.rank <= other.rank)

def greater_or_equal_to(self, other):
    return (self.rank >= other.rank)

setattr(cardgame.Card, '__eq__', equal)
setattr(cardgame.Card, '__ne__', not_equal)
setattr(cardgame.Card, '__gt__', greater_than)
setattr(cardgame.Card, '__ge__', greater_or_equal_to)
setattr(cardgame.Card, '__lt__', lower_than)
setattr(cardgame.Card, '__le__', lower_or_equal_to)

class Poker_Player(cardgame.Player):
    def __init__(self, name:str, money:int, channel):
        super().__init__(name, 0, money)
        self.channel = channel
        self.actual_bet = 0
        self.all_in = False

    def bet(self, amount:int):
        amount_subtracted = self.subtract_money(amount)
        self.actual_bet += amount_subtracted
        print(f"{self.name} betted {self.actual_bet}")
        if (amount_subtracted < amount) or (self.money == 0):
            self.all_in = True
        return amount_subtracted

class Poker_Game:
    def __init__(self, players:list):

        #table
        self.table = []

        # blinds
        self.small_blind = 0
        self.big_blind = 1
        self.actual_blind = 100

        # pot system
        self.pot = [0]
        self.actual_pot = 0

        # time system
        self.turn = 0
        self.round = 0

        # bet system
        self.actual_bet = 0

        # players system
        self.players = {}
        self.players_in_game = []
        for p in players:
            self.players[p.id] = p
            self.players_in_game.append(p.id)

    def withdraw_to_table(self, deck:cardgame.Deck):
        card = deck.withdraw_card()
        self.table.append(card)

    def increase_blind(self):
        self.actual_blind += 100

    def pass_turn(self):
        number_of_players = len(self.players_in_game)
        if self.turn + 1 == number_of_players:
            self.turn = 0
        else:
            self.turn += 1

    def pass_round(self):
        if self.round + 1 == 4:
            self.round = 0
        else:
            self.round += 1

    def pass_without_betting(self):
        if self.players[self.turn].actual_bet == self.actual_bet:
            self.pass_turn()
        else:
            raise Exception("You cannot pass untill bet {}".format(self.actual_bet))

    def fold(self):
        del self.players_in_game[self.turn]
        if self.turn >= len(self.players_in_game):
            self.turn = len(self.players_in_game) - 1
        self.pass_turn()

    def bet(self, amount:int, index = None):
        if index != None:
            player = self.players[index]
        else:
            player = self.players[self.players_in_game[self.turn]]

        if (player.actual_bet + amount > self.actual_bet) and (player.money > amount):
            amount_subtracted = player.bet(amount)
            self.pot[self.actual_pot] += amount_subtracted
            self.actual_bet = player.actual_bet

        elif (player.actual_bet + amount == self.actual_bet) and (player.money > amount):
            amount_subtracted = player.bet(amount)
            self.pot[self.actual_pot] += amount_subtracted

        elif (player.actual_bet + amount < self.actual_bet) and (player.money == amount):
            amount_subtracted = player.bet(amount)
            not_paid = self.actual_bet - amount_subtracted
            turns_passed = range(self.turn - 1)
            self.pot.append(0)
            for t in turns_passed:
                self.pot[self.actual_pot] -= not_paid
                self.pot[self.actual_pot + 1] += not_paid
            self.pot[self.actual_pot] += amount_subtracted
            self.actual_pot += 1

        elif (player.actual_bet + amount == self.actual_bet) and (player.money == amount):
            amount_subtracted = player.bet(amount)
            self.pot[self.actual_pot] += amount_subtracted
            self.pot.append(0)
            self.actual_pot += 1

        else:
            print(player.money)
            print(amount)
            print(player.actual_bet + amount)
            print(self.actual_bet)
            raise Exception("Illegal move")
        self.pass_turn()
    
    def start_game(self):
        self.actual_bet = 0
        self.turn = 0
        self.pot = 0
        self.round = 0
        self.players_in_game = []
        for p in self.players:
            self.players_in_game.append(p)

        if self.big_blind + 1 == len(self.players):
            self.big_blind = 0
        else:
            self.big_blind +=1

        if self.small_blind + 1 == len(self.players):
            self.small_blind = 0
        else:
            self.small_blind +=1

    def get_prise(self, list_of_players):
        list_of_winners = list_of_players
        for i in range(len(list_of_winners)):
            list_of_winners[i].money += self.pot[i]
        self.pot = [0]
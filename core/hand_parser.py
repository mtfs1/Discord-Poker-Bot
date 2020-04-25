import core.cardgame as cardgame
import core.poker as poker
# import cardgame
# import poker

def greater_hand(table:list, *args:list):

    list_of_points = []

    def point(table_plus_hand):
        c_sum = 0
        rank_list = []
        for card in table_plus_hand:
            rank_list.append(card.rank)
        c_sum = rank_list[0]*13**4 + rank_list[1]*13**3 + rank_list[2]*13**2 + rank_list[3]*13 + rank_list[4]
        return c_sum


    def main():
        for c in args:
            actual_hand = table + c
            points = is_royal(actual_hand)
            list_of_points.append(points)


    def is_royal(table_plus_hand):
        flag = True
        sorted_hand = sorted(table_plus_hand, reverse=True)
        current_rank = 14
        h = 10

        actual_hand = []
        hand_suits_frequency = {'Diamonds':0, 'Spades':0, 'Hearts':0, 'Clubs':0}

        for card in table_plus_hand:
            hand_suits_frequency[card.suit] += 1

        if (5 in hand_suits_frequency.values()) or (6 in hand_suits_frequency.values()) or (7 in hand_suits_frequency.values()):
            main_suit = ''

            for k in hand_suits_frequency:
                if (hand_suits_frequency[k] == 5) or (hand_suits_frequency[k] == 6) or (hand_suits_frequency[k] == 7):
                    main_suit = k

            main_suit_hand = []
            for card in table_plus_hand:
                if card.suit == main_suit:
                    main_suit_hand.append(card)
            actual_hand = sorted(main_suit_hand, reverse=True)[0:5]

            for card in actual_hand:
                if card.rank != current_rank:
                    flag = False
                    break
                else:
                    current_rank -= 1

        else:
            flag = False

        if flag:
            points = h * 13 ** 5 + point(actual_hand)
            print('Royal Straight Flush')
            print(points)
            return points
        else:
            return is_straight_flush(sorted_hand, hand_suits_frequency)
        

    def is_straight_flush(table_plus_hand, hand_suits_frequency):
        flag = True
        h = 9
        
        actual_hand = []
        if (5 in hand_suits_frequency.values()) or (6 in hand_suits_frequency.values()) or (7 in hand_suits_frequency.values()):
            main_suit = ''

            for k in hand_suits_frequency:
                if (hand_suits_frequency[k] == 5) or (hand_suits_frequency[k] == 6) or (hand_suits_frequency[k] == 7):
                    main_suit = k

            main_suit_hand = []
            for card in table_plus_hand:
                if card.suit == main_suit:
                    main_suit_hand.append(card)

            actual_hand = sorted(main_suit_hand, reverse=True)

            def test_hand_if_is_straight_flush(start, end, actual_hand, last = False):
                testing_hand = actual_hand[start:end]
                current_rank = testing_hand[0].rank
                local_flag = False
                for card in testing_hand:
                    if local_flag:
                        break
                    if card.rank !=current_rank:
                        if last:
                            return False
                        local_flag = True
                    else:
                        current_rank -= 1
                if not local_flag:
                    return True

            if len(actual_hand) == 7:
                for r in range(3):
                    if r == 0:
                        result = test_hand_if_is_straight_flush(0, 5, actual_hand)
                        if result:
                            actual_hand = actual_hand[0:5]
                            break
                    elif r == 1:
                        result = test_hand_if_is_straight_flush(1, 6, actual_hand)
                        if result:
                            actual_hand = actual_hand[1:6]
                            break
                    else:
                        result = test_hand_if_is_straight_flush(2, 7, actual_hand, True)
                        actual_hand = actual_hand[2:7]
                        if not result:
                            flag = False
            elif len(actual_hand) == 6:
                for r in range(2):
                    if r == 0:
                        result = test_hand_if_is_straight_flush(0, 5, actual_hand)
                        if result:
                            actual_hand = actual_hand[0:5]
                            break
                    else:
                        result = test_hand_if_is_straight_flush(1, 6, actual_hand, True)
                        actual_hand = actual_hand[1:6]
                        if not result:
                            flag = False
            elif len(actual_hand) == 5:
                result = test_hand_if_is_straight_flush(0, 5, actual_hand, True)
                actual_hand = actual_hand[0:5]
                if not result:
                    flag = False
        else:
            flag = False

        if flag:
            points = h * 13 ** 5 + point(actual_hand)
            print('Straight Flush')
            print(points)
            return points
        else:
            return is_four(table_plus_hand, hand_suits_frequency)


    def is_four(table_plus_hand, hand_suits_frequency):
        flag = True
        h = 8

        hand_ranks_frequency = {2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0}

        for card in table_plus_hand:
            hand_ranks_frequency[card.rank] += 1

        if 4 in hand_ranks_frequency.values():
            actual_hand = []

            four_rank = 0
            for rank in hand_ranks_frequency:
                if hand_ranks_frequency[rank] == 4:
                    four_rank = rank
            
            for card in table_plus_hand:
                if card.rank == four_rank:
                    actual_hand.append(card)

            i = 14
            higher_rank_besides_four_rank = 0
            while True:
                if hand_ranks_frequency[i] not in (4, 0):
                    higher_rank_besides_four_rank = i
                    break
                i -= 1

            for card in table_plus_hand:
                if card.rank == higher_rank_besides_four_rank:
                    actual_hand.append(card)
                    break

        else:
            flag = False

        if flag:
            points = h * 13 ** 5 + point(actual_hand)
            print('Four of a Kind')
            print(points)
            return points
        else:
            return is_full_house(table_plus_hand, hand_suits_frequency, hand_ranks_frequency)


    def is_full_house(table_plus_hand, hand_suits_frequency, hand_ranks_frequency):
        flag = True
        h = 7

        ranks_that_appear_two_times = []
        ranks_that_appear_three_times = []
        
        for rank in hand_ranks_frequency:
            if hand_ranks_frequency[rank] == 3:
                ranks_that_appear_three_times.append(rank)
            elif hand_ranks_frequency[rank] == 2:
                ranks_that_appear_two_times.append(rank)

        quantity_of_three_of_a_kind = len(ranks_that_appear_three_times)
        quantity_of_pairs = len(ranks_that_appear_two_times)

        actual_hand = []
        if quantity_of_three_of_a_kind == 1:

            if quantity_of_pairs > 0:

                for card in table_plus_hand:
                    if card.rank == ranks_that_appear_three_times[0]:
                        actual_hand.append(card)
                
                rank_of_full_house_pair = ranks_that_appear_two_times[-1]
                for card in table_plus_hand:
                    if card.rank == rank_of_full_house_pair:
                        actual_hand.append(card)

            else:
                flag = False

        elif quantity_of_three_of_a_kind == 2:

            rank_of_full_house_three_of_a_kind = ranks_that_appear_three_times[1]
            rank_of_full_house_pair = ranks_that_appear_three_times[0]

            for card in table_plus_hand:
                if card.rank == rank_of_full_house_three_of_a_kind:
                    actual_hand.append(card)
            for card in table_plus_hand:
                if card.rank == rank_of_full_house_pair:
                    actual_hand.append(card)

        else:
            flag = False

        if flag:
            points = h * 13 ** 5 + point(actual_hand)
            print('Full House')
            print(points)
            return points
        else:
            return is_flush(table_plus_hand, hand_suits_frequency, hand_ranks_frequency)


    def is_flush(table_plus_hand, hand_suits_frequency, hand_ranks_frequency):
        flag = True
        h = 6

        actual_hand = []
        current_suit = ''

        for s in hand_suits_frequency:
            if hand_suits_frequency[s] in [5, 6, 7]: 
                current_suit = s
        
        if current_suit == '':
            flag = False
        else:
            for c in table_plus_hand:
                if c.suit == current_suit:
                    actual_hand.append(c)

            actual_hand = actual_hand[0:5]

        if flag:
            points = h * 13 ** 5 + point(actual_hand)
            print('Flush')
            print(points)
            return points
        else:
            return is_straight(table_plus_hand, hand_suits_frequency, hand_ranks_frequency)

    
    def is_straight(table_plus_hand, hand_suits_frequency, hand_ranks_frequency):
        flag = True
        h = 5

        repeated_ranks = []
        for r in hand_ranks_frequency:
            if hand_ranks_frequency[r] > 1:
                repeated_ranks.append(r)

        hand_without_repeated_ranks = []
        for c in table_plus_hand:
            if c.rank in repeated_ranks:
                pass
            hand_without_repeated_ranks.append(c)

        def test_hand_if_is_straight(start, end, actual_hand, last = False):
            testing_hand = actual_hand[start:end]
            current_rank = testing_hand[0].rank
            local_flag = False
            for card in testing_hand:
                if local_flag:
                    break
                if card.rank !=current_rank:
                    if last:
                        return False
                    local_flag = True
                else:
                    current_rank -= 1
            if not local_flag:
                actual_hand = testing_hand
                return True
        
        actual_hand = []
        if len(hand_without_repeated_ranks) == 7:
            for r in range(3):
                if r == 0:
                    result = test_hand_if_is_straight(0, 5, hand_without_repeated_ranks)
                    if result:
                        actual_hand = hand_without_repeated_ranks[0:5]
                        break
                elif r == 1:
                    result = test_hand_if_is_straight(1, 6, hand_without_repeated_ranks)
                    if result:
                        actual_hand = hand_without_repeated_ranks[1:6]
                        break
                else:
                    result = test_hand_if_is_straight(2, 7, hand_without_repeated_ranks, True)
                    actual_hand = hand_without_repeated_ranks[2:7]
                    if not result:
                        flag = False
        elif len(hand_without_repeated_ranks) == 6:
            for r in range(2):
                if r == 0:
                    result = test_hand_if_is_straight(0, 5, hand_without_repeated_ranks)
                    if result:
                        actual_hand = hand_without_repeated_ranks[0:5]
                        break
                elif r == 1:
                    result = test_hand_if_is_straight(1, 6, hand_without_repeated_ranks, True)
                    actual_hand = hand_without_repeated_ranks[1:6]
                    if not result:
                        flag = False
        elif len(hand_without_repeated_ranks) == 5:
            result = test_hand_if_is_straight(0, 5, hand_without_repeated_ranks, True)
            actual_hand = hand_without_repeated_ranks[0:5]
            if not result:
                flag = False

        if flag:
            points = h * 13 ** 5 + point(actual_hand)
            print('Straight')
            print(points)
            return points
        else:
            return is_three(table_plus_hand, hand_suits_frequency, hand_ranks_frequency)
    

    def is_three(table_plus_hand, hand_suits_frequency, hand_ranks_frequency):
        flag = True
        h = 4

        three_of_a_kind = -1
        for r in hand_ranks_frequency:
            if hand_ranks_frequency[r] == 3:
                three_of_a_kind = r
            
        if three_of_a_kind != -1:
            actual_hand = []
            for c in table_plus_hand:
                if c.rank == three_of_a_kind:
                    actual_hand.append(c)

            current_rank = 14
            ranks_breaker = []
            while True:
                if len(ranks_breaker) == 2:
                    break
                if hand_ranks_frequency[current_rank] not in [0, 3]:
                    ranks_breaker.append(current_rank)
                current_rank -= 1

            for card in table_plus_hand:
                if card.rank in ranks_breaker:
                    actual_hand.append(card)
                
        else:
            flag = False

        if flag:
            points = h * 13 ** 5 + point(actual_hand)
            print('Three of a Kind')
            print(points)
            return points 
        else:
            return is_two(table_plus_hand, hand_suits_frequency, hand_ranks_frequency)


    def is_two(table_plus_hand, hand_suits_frequency, hand_ranks_frequency):
        flag = True
        h = 3

        pairs = []
        for r in hand_ranks_frequency:
            if hand_ranks_frequency[r] == 2:
                pairs.append(r)

        if len(pairs) >= 2:
            actual_hand = []
            for card in table_plus_hand:
                if len(actual_hand) == 4:
                    break
                if card.rank in pairs:
                    actual_hand.append(card)

            for card in table_plus_hand:
                if card.rank not in pairs:
                    actual_hand.append(card)
                    break

        else:
            flag = False

        if flag:
            points = h * 13 ** 5 + point(actual_hand)
            print('Two Pairs')
            print(points)
            return points 
        else:
            return is_one(table_plus_hand, hand_suits_frequency, hand_ranks_frequency)


    def is_one(table_plus_hand, hand_suits_frequency, hand_ranks_frequency):
        flag = True
        h = 2

        pair = -1
        for r in hand_ranks_frequency:
            if hand_ranks_frequency[r] == 2:
                pair = r

        if pair != -1:
            actual_hand = []
            for card in table_plus_hand:
                if card.rank == pair:
                    actual_hand.append(card)
            
            for card in table_plus_hand:
                if len(actual_hand) == 5:
                    break
                if card.rank != pair:
                    actual_hand.append(card)

        else:
            flag = False

        if flag:
            points = h * 13 ** 5 + point(actual_hand)
            print('One Pair')
            print(points)
            return points
        else:
            return is_high(table_plus_hand)

    def is_high(table_plus_hand):
        actual_hand = table_plus_hand[0:5]
        h = 1

        points = h * 13 ** 5 + point(actual_hand)
        print('High')
        print(points)
        return points
    main()

deck = cardgame.Deck()
deck.shuffle()

table = []
table.append(deck.withdrawCard())
table.append(deck.withdrawCard())
table.append(deck.withdrawCard())
table.append(deck.withdrawCard())
table.append(deck.withdrawCard())

hand1 = []
hand1.append(deck.withdrawCard())
hand1.append(deck.withdrawCard())

hand2 = []
hand2.append(deck.withdrawCard())
hand2.append(deck.withdrawCard())

hand3 = []
hand3.append(deck.withdrawCard())
hand3.append(deck.withdrawCard())

print('-------')
for card in table + hand1:
    print(card)
print('-------')
for card in table + hand2:
    print(card)
print('-------')
for card in table + hand3:
    print(card)
print('-------')
greater_hand(table, hand1, hand2, hand3)

# tableTest = []
# tableTest.append(cardgame.Card(5, 'Spades'))
# tableTest.append(cardgame.Card(10, 'Hearts'))
# tableTest.append(cardgame.Card(4, 'Hearts'))
# tableTest.append(cardgame.Card(8, 'Diamonds'))
# tableTest.append(cardgame.Card(12, 'Hearts'))

# handTest = []
# handTest.append(cardgame.Card(8, 'Hearts'))
# handTest.append(cardgame.Card(2, 'Spades'))

# handTestTwo= []
# handTestTwo.append(cardgame.Card(4, 'Diamonds'))
# handTestTwo.append(cardgame.Card(9, 'Clubs'))

# greater_hand(tableTest, handTest, handTestTwo)

# p1 = PokerPlayer("John", 1200, "a")
# p2 = PokerPlayer("Bob", 1200, "a")
# p3 = PokerPlayer("Isac", 10, "a")
# players = []
# players.append(p1)            
# players.append(p2)            
# players.append(p3)

# game = PokerGame(players)
# print(game.pot)
# game.bet(10)
# game.bet(10)
# game.bet(10)
# print(game.pot)
# game.bet(10)
# game.bet(10)
# print(game.pot)

# listOfWinners = [game.players[0], game.players[2]]
# game.getPrise(listOfWinners)
# print(game.players[0].money)
# print(game.players[1].money)
# print(game.players[2].money)
# print(game.pot)
# print(game.actualBet)
# print(game.turn)
# print(game.players[0].money)
# print(game.players[0].actualBet)
import discord
from discord.ext import commands

import core.poker as poker
import core.cardgame as cardgame
import core.hand_parser as hand_parser_module


async def play_game(ctx:commands.context, client:commands.Bot, list_of_users:dict):

    deck = cardgame.Deck()
    separator = 30 * "-"


    async def wait_for_response(message, name, ctx, func = False):
        await ctx.send(message)
        while True:
            response = await client.wait_for("message")
            author = response.author.name
            content = response.content
            if author == name:
                if not func:
                    return content
                else:
                    if func(content):
                        return content
    

    async def flow():
        game = create_game()
        await bet_round(game, 3)
        await bet_round(game, 1)
        await bet_round(game, 1)
        await bet_round(game, 0)
        await hand_parser(game)


    def create_game():
        list_of_players = []

        for u in list_of_users:
            p1 = poker.Poker_Player(u, 2000, list_of_users[u])
            list_of_players.append(p1)

        game = poker.Poker_Game(list_of_players)
        return game


    async def bet_round(game:poker.Poker_Game, cards_to_table:int):
        if cards_to_table == 3:
            await ctx.send(f"Big blind: {game.players[game.big_blind].name}\n"
                        f"Small blind: {game.players[game.small_blind].name}\n"
                        f"{separator}")
            game.bet(game.actual_blind/2, game.small_blind)
            game.bet(game.actual_blind, game.big_blind)
            deck.shuffle()

            for p in game.players:
                player = game.players[p]
                player.withdraw_card(deck)
                player.withdraw_card(deck)

                await player.channel.send(separator)
                await player.channel.send(f"You have the amount of {player.money} chips")
                await player.channel.send(player.hand[0].return_card())
                await player.channel.send(player.hand[1].return_card())

        game.last_to_raise = 0
        game.flag = False

        while not game.flag:
            p = game.turn
            player = game.players[p]
            need_to_bet = game.actual_bet - player.actual_bet


            async def call(game:poker.Poker_Game, ctx, need_to_bet):
                game.bet(need_to_bet)
                return False


            async def raise_bet(game:poker.Poker_Game, ctx, need_to_bet):
                message = "How much do you want to raise?"
                name = player.name
                def is_number(s):
                    try:
                        float(s)
                        return True
                    except ValueError:
                        return False
                raise_value = float(await wait_for_response(message, name, ctx, is_number))
                game.bet(need_to_bet + raise_value)
                game.last_to_raise = p
                return False


            async def pass_turn(game:poker.Poker_Game, ctx, need_to_bet):
                if game.turn == game.last_to_raise:
                    game.pass_without_betting()
                    return True
                game.pass_without_betting()


            async def fold(game:poker.Poker_Game, ctx, need_to_bet):
                game.fold()
                return True


            options = {
                "c": call,
                "r": raise_bet,
                "p": pass_turn,
                "f": fold
            }


            if not player.all_in:
                if need_to_bet != 0:
                    message = f"{player.name} needs to bet {need_to_bet}\nDo you want to call, raise or fold?\n[c] call\n[r] raise\n[f] fold"
                    name = player.name
                    def is_valid(s): return s.lower() in ["c", "r", "f"]
                    r = await wait_for_response(message, name, ctx, is_valid)
                    await options[r.lower()](game, ctx, need_to_bet)
                else:
                    message = f"{player.name} don't need to bet\nDo you want to pass, raise or fold?\n[p] pass\n[r] raise\n[f] fold"
                    name = player.name
                    def is_valid(s): return s.lower() in ["p", "r", "f"]
                    r = await wait_for_response(message, name, ctx, is_valid)
                    value = await options[r.lower()](game, ctx, need_to_bet)
                    if value: game.flag = True

            
        await ctx.send(separator)


        for c in range(cards_to_table):
            game.withdraw_to_table(deck)
        

        for c in game.table:
            await ctx.send(f"{c}")

        await ctx.send(separator)


    async def hand_parser(game):
        table = game.table
        hands = [] 
        for p in game.players:
            hands.append(game.players[p].hand)
        points = hand_parser_module.greater_hand(table, hands)
        winner_points = max(points)
        winner_index = points.index(winner_points)
        await ctx.send(f"{game.players[winner_index].name} won the round!")


    await flow()
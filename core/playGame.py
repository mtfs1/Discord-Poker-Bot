import discord
from discord.ext import commands

import core.poker as poker
import core.cardgame as cardgame

async def play_game(ctx:commands.context, client:commands.Bot, list_of_users:dict):

    deck = cardgame.Deck()
    separator = 30 * "-"
    
    async def flow():
        game = create_game()
        await first_bet_round(game)
        # secondBetRound()
        # thirdBetRound()
        # fourthBetRound()

    def create_game():
        list_of_players = []

        for u in list_of_users:
            p1 = poker.Poker_Player(u, 2000, list_of_users[u])
            list_of_players.append(p1)

        game = poker.Poker_Game(list_of_players)
        return game


    async def first_bet_round(game:poker.Poker_Game):
        await ctx.send(f"Big blind: {game.players[game.big_blind].name}\n"
                       f"Small blind: {game.players[game.small_blind].name}\n"
                       f"{separator}")
        game.bet(game.actual_blind/2, game.small_blind)
        print(f"game actual bet is {game.actual_bet}")
        game.bet(game.actual_blind, game.big_blind)
        print(f"game actual bet is {game.actual_bet}")
        deck.shuffle()
        game.last_to_raise = 0

        for p in game.players:
            player = game.players[p]
            player.withdraw_card(deck)
            await player.channel.send(f"You have the amount of {player.money} chips")
            await player.channel.send(player.hand[0].return_card())
            player.withdraw_card(deck)
            await player.channel.send(player.hand[1].return_card())

        game.flag = False

        while not game.flag:
            p = game.turn
            player = game.players[p]

            print(f"turn of the player {p}")
            print(f"{player.name} betted {player.actual_bet}")
            print(f"game actual bet is {game.actual_bet}")
            
            need_to_bet = game.actual_bet - player.actual_bet


            async def call(game:poker.Poker_Game, ctx, need_to_bet):
                game.bet(need_to_bet)
                return False


            async def raise_bet(game:poker.Poker_Game, ctx, need_to_bet):
                await ctx.send('How much do you want to raise?')
                while True:
                    message2 = await client.wait_for('message')
                    if message2.author.name == player.name:
                        try:
                            raise_value = int(message2.content)
                        except ValueError:
                            try:
                                raise_value = float(message2.content)
                            except ValueError:
                                continue
                        game.bet(need_to_bet + raise_value)
                        game.last_to_raise = p
                    break
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


            if (need_to_bet != 0) and (not player.all_in):
                await ctx.send(f"{player.name} needs to bet {need_to_bet}")
                await ctx.send("Do you want to call, raise or fold?\n[c] call\n[r] raise\n[f] fold")
                while True:
                    message = await client.wait_for("message")
                    if (message.author.name == player.name) and (message.content.lower() in ['c', 'r', 'f']):
                        await options[message.content.lower()](game, ctx, need_to_bet)
                        break
            elif (need_to_bet == 0) and (not player.all_in):
                await ctx.send(f"{player.name} don't need to bet")
                await ctx.send("Do you want to pass, raise or fold?\n[p] pass\n[r] raise\n[f] fold")
                while True:
                    message = await client.wait_for("message")
                    author = message.author.name
                    if (author == player.name) and (message.content.lower() in ['p', 'r', 'f']):
                        value = await options[message.content.lower()](game, ctx, need_to_bet)
                        print(value)
                        if value:
                            game.flag = True
                        break
            
        await ctx.send(separator)

        game.withdraw_to_table(deck)
        game.withdraw_to_table(deck)
        game.withdraw_to_table(deck)

        for c in game.table:
            await ctx.send(f"{c}")

        await ctx.send(separator)

    await flow()
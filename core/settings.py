import discord
from discord.ext import commands
import pprint

async def settings(ctx:commands.context, client:commands.Bot):
    await ctx.send("Who are the players we have?")
    players ={}
    while True:
        message = await client.wait_for("message")
        if message.channel == ctx.channel:
            if message.content.lower() == "me":
                if message.author.name in players:
                    await ctx.send(f"{message.author.name}, you're already in the game")
                else:
                    players[message.author.name] = await message.author.create_dm()
            elif message.content.lower() == "ok":
                if len(players) < 2:
                    await ctx.send("It's necessary at least two players to the game")
                else:
                    break
    return players
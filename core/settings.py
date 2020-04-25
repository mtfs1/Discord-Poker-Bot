import discord
from discord.ext import commands
import pprint

async def settings(ctx:commands.context, client:commands.Bot):
    await ctx.send("Who are the players that we have?")
    players ={}
    while True:
        message = await client.wait_for("message")
        if message.channel == ctx.channel:
            if message.content.lower() == 'me':
                if message.author.name in players:
                    await ctx.send("{}, you're already in the game".format(message.author.name))
                else:
                    players[message.author.name] = await message.author.create_dm()
            elif message.content.lower() == 'enough':
                break
    return players
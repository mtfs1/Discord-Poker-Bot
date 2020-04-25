from core.settings import settings
from core.playGame import play_game
import credentials


import discord
from discord.ext import commands


client = commands.Bot(command_prefix = '>')


@client.event
async def on_ready():
    print("Bot connected")


@client.command()
async def poker(ctx):
    players = await settings(ctx, client)
    await play_game(ctx, client, players)


@client.command()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount+1)


client.run(credentials.discordToken)
import discord
from discord.ext import commands, tasks

import random

# Commands to flip a coin or roll a dice
class diceFlipCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def flip(self, ctx):
        mention = ctx.author.mention
        flip = random.randint(0, 1)
        if (flip == 0):
            await ctx.channel.send(mention + ' `flips heads` ')
        else:
            await ctx.channel.send(mention + ' `flips tails` ')

    @commands.command()
    async def dice(self, ctx):
        mention = ctx.author.mention
        dice = random.randint(1, 6)
        await ctx.channel.send(mention + f' `rolls {str(dice)}` ')

# Sets up the bot commands above
def setup(bot):
    bot.add_cog(diceFlipCommands(bot))
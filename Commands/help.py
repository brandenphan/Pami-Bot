import discord
from discord.ext import commands, tasks

# Command to show user the various commands supported by the bot
class helpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embedVar = discord.Embed(title='Pami Help', description='Pami contains various features and commands that are prefixed with \'$\'', color=0x3e7ada)
        embedVar.add_field(name='To-do', value='Contains various commands for your personal to-do list, type \'$todo help\' for the full list of commands', inline=False)
        embedVar.add_field(name='Stocks', value='$stock \'stock name\' will return the price of the stock, showing green if the stock is up for the day and red if the stock is down for the day', inline=False)
        embedVar.add_field(name='Crypto', value='$crypto \'coin name\' will return the price of the cryptocurrency coin', inline=False)
        embedVar.add_field(name='Google', value='$google \'something\' will google search for \'something\' returning the first link found', inline=False)
        embedVar.add_field(name='Wiki', value='$wiki \'something\' will search for \'something\' on wikipedia, returning the first section of information on the page', inline=False)
        embedVar.add_field(name='Flip', value='$flip will flip a coin, resulting in heads or tails', inline=False)
        embedVar.add_field(name='Dice', value='$dice will roll a die, resulting in a number between 1-6', inline=False)
        embedVar.add_field(name='Trivia', value='$trivia will display a question to the user and specifications for the question. The bot will then prompt the user to enter an answer, displaying if the user\'s answer was correct or not', inline=False)
        embedVar.add_field(name='Join and Leave', value='$join will get the bot to join the users current voice channel and $leave will get the bot to leave the voice channel', inline=False)
        embedVar.add_field(name='Music', value='Contains various commands for music control with youtube, type \'$music help\' for the full list of commands', inline=False)
        embedVar.add_field(name='Say', value='$say \'phrase\' will get the bot to say the \'phrase\' in the voice channel', inline=False)
        embedVar.add_field(name='Tetrio', value='$tetrioProfile \'name\' will display information regarding the profile entered by the user', inline=False)
        embedVar.add_field(name='Brawlhalla', value='Contains various commands regarding Brawlhalla, type \'$brawl Help\' for the full list of commands')
        await ctx.channel.send(embed=embedVar)

# Sets up the bot command above
def setup(bot):
    bot.add_cog(helpCommand(bot))
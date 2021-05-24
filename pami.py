import os

import discord
from discord.ext import commands, tasks
from discord.ext.commands import CommandNotFound

# Imports environment variables from discordTokens.env
from dotenv import load_dotenv
load_dotenv("discordTokens.env")
DISCORD_TOKEN = os.getenv("discord_token") 

bot = commands.Bot(command_prefix='$')

# Removes the built in Discordpy help command
bot.remove_command('help')

# Imports bot commands from Commands package
startupExtensions = ['Commands.diceFlip', 'Commands.trivia', 'Commands.stockCrypto', 'Commands.tetrio', 'Commands.brawlhalla', 'Commands.todo', 'Commands.search', 'Commands.music', 'Commands.say', 'Commands.help']
for extensions in startupExtensions:
    bot.load_extension(extensions)


@bot.event  # Event when the bot is logged in
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


# Handles the event if the user enters a command that does not exist 
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        mention = ctx.author.mention
        embedVar = discord.Embed(description=f'You entered a command that does not exist, use \'$help\' for the list of commands {mention}', color=0x3e7ada)
        await ctx.channel.send(embed=embedVar)
        return
    raise error

bot.run(DISCORD_TOKEN);  
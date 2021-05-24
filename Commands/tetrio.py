import discord
from discord.ext import commands, tasks

import requests
import json

# Commands to view Tetrio Profiles
class tetrioCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def tetrioProfile(self, ctx, name=None):
        mention = ctx.author.mention

        if name is None:
            embedVar = discord.Embed(description=f'Can\'t search for an empty profile name {mention}', color=0x9932CC)
            await ctx.channel.send(embed=embedVar)
        else:
            # Gets the user information from the Tetrio API endpoint
            profileName = name.lower()
            profileString = requests.get(f'https://ch.tetr.io/api//users/{profileName}')
            profileJSON = json.loads(profileString.text)

            # Ensure the profile exist and displays various information regarding the user
            if profileJSON['success'] == True:
                name = profileJSON['data']['user']['username']
                xp = profileJSON['data']['user']['xp']
                country = profileJSON['data']['user']['country']
                totalGamesPlayed = profileJSON['data']['user']['gamesplayed']
                totalGamesWon = profileJSON['data']['user']['gameswon']
                playTime = profileJSON['data']['user']['gametime']

                leagueLeaderBoard = profileJSON['data']['user']['league']['standing']
                leagueGamesPlayed = profileJSON['data']['user']['league']['gamesplayed']
                leagueGamesWon = profileJSON['data']['user']['league']['gameswon']
                leagueRating = profileJSON['data']['user']['league']['rating']
                leagueRank = profileJSON['data']['user']['league']['rank'].upper()
                leagueAPM = profileJSON['data']['user']['league']['apm']
                leaguePPS = profileJSON['data']['user']['league']['pps']

                profileStats = f'Name: {name}\nExp: {xp}\nCountry: {country}\nTotal Games Played: {totalGamesPlayed}\nTotal Games Won: {totalGamesWon}\nPlay Time: {playTime:.2f} seconds\n\nTetra League:\nRank: {leagueRank}\nRating: {leagueRating:.0f}\nLeaderboard: {leagueLeaderBoard}\nGames Played: {leagueGamesPlayed}\nGames Won: {leagueGamesWon}\nAPM: {leagueAPM}\nPPS: {leaguePPS}'

                embedVar = discord.Embed(title='Tetrio Profile', description=f'{profileStats}', color=0x9932CC)
                await ctx.channel.send(embed=embedVar)
            else:
                embedVar = discord.Embed(description=f'{name} profile does not exist {mention}', color=0x9932CC)
                await ctx.channel.send(embed=embedVar)

# Sets up the bot command above
def setup(bot):
    bot.add_cog(tetrioCommands(bot))

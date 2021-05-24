import discord
from discord.ext import commands, tasks

import requests
import json
import os

# Imports environment variables from discordTokens.env
from dotenv import load_dotenv
load_dotenv('../discordTokens.env')
BRAWLHALLA_KEY = os.getenv('brawlhalla_key')

# Commands regarding the game Brawlhalla
class brawlhallaCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def brawlLegend(self, ctx, name=None):
        mention = ctx.author.mention

        if name is None:
            embedVar = discord.Embed(description=f'Can\'t search for an empty brawlhalla character {mention}', color=0x008080)
            await ctx.channel.send(embed=embedVar)
        else:
            # Gets all the characters information from Brawlhalla API endpoint
            searchCharName = name.lower()
            allCharactersResponse = requests.get(f'https://api.brawlhalla.com/legend/all/?api_key={BRAWLHALLA_KEY}')
            allCharacters = json.loads(allCharactersResponse.text)
            characterExist = 0

            # Gets the information of the character specified by the user
            for character in allCharacters:
                if character['legend_name_key'] == searchCharName:
                    characterExist = 1
                    characterInformation = character
            
            if characterExist == 1:
                legendName = characterInformation['legend_name_key']
                legendBio = characterInformation['bio_aka']
                legendW1 = characterInformation['weapon_one']
                legendW2 = characterInformation['weapon_two']
                legendStr = characterInformation['strength']
                legendDex = characterInformation['dexterity']
                legendDef = characterInformation['defense']
                legendSpeed = characterInformation['speed']

                characterStats = f'Name: {legendName.capitalize()}\nBio: {legendBio}\nWeapon 1: {legendW1}\nWeapon 2: {legendW2}\nStrength: {legendStr}\nDexterity: {legendDex}\nDefense: {legendDef}\nSpeed: {legendSpeed}'

                embedVar = discord.Embed(title=f'Brawlhalla Character Stats:', description=f'{characterStats}', color=0x008080)
                await ctx.channel.send(embed=embedVar)
            else:
                embedVar = discord.Embed(description=f'{name} character does not exist {mention}', color=0x008080)
                await ctx.channel.send(embed=embedVar)
    
    @commands.command()
    async def brawlWeaponSearch(self, ctx, weapon1=None, weapon2=None):
        mention = ctx.author.mention

        if weapon1 is None and weapon2 is None:
            embedVar = discord.Embed(description=f'Can\'t search for a character with 2 empty weapons {mention}', color=0x008080)
            await ctx.channel.send(embed=embedVar)
        elif weapon2 is None:
            # Changing to the specific weapon names specified by the brawlhalla API
            if weapon1 == 'blaster':
                weaponName = 'pistol'
            elif weapon1 == 'gauntlet':
                weaponName = 'fists'
            else:
                weaponName = weapon1

            # Ensuring the user enters a proper weapon name
            if weaponName == 'hammer' or weaponName == 'sword' or weaponName == 'pistol' or weaponName == 'lance' or weaponName == 'spear' or weaponName == 'katar' or weaponName == 'axe' or weaponName == 'bow' or weaponName == 'fists' or weaponName == 'scythe' or weaponName == 'cannon' or weaponName == 'orb' or weaponName == 'greatsword':
                
                # Gets the information on each character from the brawlhalla API endpoint
                searchWeapon1 = weaponName.lower()
                allCharactersResponse = requests.get(f'https://api.brawlhalla.com/legend/all/?api_key={BRAWLHALLA_KEY}')
                allCharacters = json.loads(allCharactersResponse.text)

                charactersWithWeapons = []
                for character in allCharacters:
                    if character['weapon_one'].lower() == searchWeapon1 or character['weapon_two'].lower() == searchWeapon1:
                        charactersWithWeapons.append(character)

                characterStats = ""
                for character in charactersWithWeapons:
                    characterName = character['legend_name_key'].capitalize()
                    characterStats += f'{characterName}\n'

                embedVar = discord.Embed(title=f'Brawlhalla characters with {weapon1}: ', description=f'{characterStats}', color=0x008080)
                await ctx.channel.send(embed=embedVar)
            else:
                embedVar = discord.Embed(description=f'{weapon1} weapon does not exist, the list of current weapon names are: hammer, sword, pistol/blaster, lance, spear, katar, axe, bow, fists/gauntlet, scythe, cannon, orb, greatsword {mention}', color=0x008080)
                await ctx.channel.send(embed=embedVar)
        else:
            # Changing to the specific weapon names specified by the brawlhalla API
            if weapon1 == 'blaster':
                weaponName1 = 'pistol'
            elif weapon1 == 'gauntlet':
                weaponName1 = 'fists'
            else:
                weaponName1 = weapon1
            if weapon2 == 'blaster':
                weaponName2 = 'pistol'
            elif weapon2 == 'gauntlet':
                weaponName2 = 'fists'
            else:
                weaponName2 = weapon2

            # Ensuring the user enters a proper weapon name
            if weaponName1 == 'hammer' or weaponName1 == 'sword' or weaponName1 == 'pistol' or weaponName1 == 'lance' or weaponName1 == 'spear' or weaponName1 == 'katar' or weaponName1 == 'axe' or weaponName1 == 'bow' or weaponName1 == 'fists' or weaponName1 == 'scythe' or weaponName1 == 'cannon' or weaponName1 == 'orb' or weaponName1 == 'greatsword' and weaponName2 == 'hammer' or weaponName2 == 'sword' or weaponName2 == 'pistol' or weaponName2 == 'lance' or weaponName2 == 'spear' or weaponName2 == 'katar' or weaponName2 == 'axe' or weaponName2 == 'bow' or weaponName2 == 'fists' or weaponName2 == 'scythe' or weaponName2 == 'cannon' or weaponName2 == 'orb' or weaponName2 == 'greatsword':

                # Gets the information on each character from the brawlhalla API endpoint
                searchWeapon1 = weaponName1.lower()
                searchWeapon2 = weaponName2.lower()
                allCharactersResponse = requests.get(f'https://api.brawlhalla.com/legend/all/?api_key={BRAWLHALLA_KEY}')
                allCharacters = json.loads(allCharactersResponse.text)     

                charactersWithWeapons = []
                for character in allCharacters:
                    if character['weapon_one'].lower() == searchWeapon1 and character['weapon_two'].lower() == searchWeapon2:
                        charactersWithWeapons.append(character)
                    elif character['weapon_one'].lower() == searchWeapon2 and character['weapon_two'].lower() == searchWeapon1:
                        charactersWithWeapons.append(character)

                if len(charactersWithWeapons) == 0:
                    embedVar = discord.Embed(description=f'{mention} There are no legends with {weapon1} and {weapon2}', color=0x008080)
                    await ctx.channel.send(embed=embedVar)
                else:
                    characterStats = ""
                    for character in charactersWithWeapons:
                        characterName = character['legend_name_key'].capitalize()
                        characterStats += f'{characterName}\n'

                    embedVar = discord.Embed(title=f'Brawlhalla characters with {weapon1} and {weapon2}: ', description=f'{characterStats}', color=0x008080)
                    await ctx.channel.send(embed=embedVar)
            else:
                if not weapon1 == 'hammer' or weaponName1 == 'sword' or weaponName1 == 'pistol' or weaponName1 == 'lance' or weaponName1 == 'spear' or weaponName1 == 'katar' or weaponName1 == 'axe' or weaponName1 == 'bow' or weaponName1 == 'fists' or weaponName1 == 'scythe' or weaponName1 == 'cannon' or weaponName1 == 'orb' or weaponName1 == 'greatsword':
                    embedVar = discord.Embed(description=f'{weapon1} weapon does not exist, the list of current weapon names are: hammer, sword, pistol/blaster, lance, spear, katar, axe, bow, fists/gauntlet, scythe, cannon, orb, greatsword {mention}', color=0x008080)
                    await ctx.channel.send(embed=embedVar)
                elif not weaponName2 == 'hammer' or weaponName2 == 'sword' or weaponName2 == 'pistol' or weaponName2 == 'lance' or weaponName2 == 'spear' or weaponName2 == 'katar' or weaponName2 == 'axe' or weaponName2 == 'bow' or weaponName2 == 'fists' or weaponName2 == 'scythe' or weaponName2 == 'cannon' or weaponName2 == 'orb' or weaponName2 == 'greatsword':
                    embedVar = discord.Embed(description=f'{weapon2} weapon does not exist, the list of current weapon names are: hammer, sword, pistol/blaster, lance, spear, katar, axe, bow, fists/gauntlet, scythe, cannon, orb, greatsword {mention}', color=0x008080)
                    await ctx.channel.send(embed=embedVar)
                else:
                    embedVar = discord.Embed(description=f'{weapon1} and {weapon2} weapons do not exist, the list of current weapon names are: hammer, sword, pistol/blaster, lance, spear, katar, axe, bow, fists/gauntlet, scythe, cannon, orb, greatsword {mention}', color=0x008080)
                    await ctx.channel.send(embed=embedVar)

    @commands.command()
    async def brawlProfile(self, ctx, userID=None):
        mention = ctx.author.mention

        if userID is None:
            embedVar = discord.Embed(description=f'Cannot have an empty brawlhalla profile to search for {mention}', color=0x008080)
            await ctx.channel.send(embed=embedVar)
        else:
            # Gets the data from the brawlhalla API endpoint regarding the userID inputted by the user
            profileResponse = requests.get(f'https://api.brawlhalla.com/player/{userID}/stats?api_key={BRAWLHALLA_KEY}')
            profile = json.loads(profileResponse.text)

            rankedProfileResponse = requests.get(f'https://api.brawlhalla.com/player/{userID}/ranked?api_key={BRAWLHALLA_KEY}')
            rankedProfile = json.loads(rankedProfileResponse.text)

            # Checks to see if the profile exist
            if len(profile) == 0 or len(profile) == 1:
                embedVar = discord.Embed(description=f'Profile with {userID} does not exist {mention}', color=0x008080)
                await ctx.channel.send(embed=embedVar)
            else:
                profileName = profile['name']
                profileLevel = profile['level']
                profileTotalGamesPlayed = profile['games']
                profileTotalGamesWon = profile['wins']

                profileStats = f'Name: {profileName}\nLevel: {profileLevel}\nTotal Games Played: {profileTotalGamesPlayed}\nTotal Games Won: {profileTotalGamesWon}'

                # If the user profile has ranked stats, displays them as well as the general profile stats
                if len(rankedProfile) != 0 and len(rankedProfile) != 1:
                    rankedRating = rankedProfile['rating']
                    rankedPeakRating = rankedProfile['peak_rating']
                    rankedTier = rankedProfile['tier']
                    rankedWins = rankedProfile['wins']
                    rankedGames = rankedProfile['games']

                    rankedProfileStats = f'Rating: {rankedRating}\nPeak Rating: {rankedPeakRating}\nTier: {rankedTier}\nWins: {rankedWins}\nNumber of Games: {rankedGames}'

                    embedVar = discord.Embed(title='Brawlhalla Profile', description=f'{profileStats}\n\nRanked:\n{rankedProfileStats}', color=0x008080)
                    await ctx.channel.send(embed=embedVar)
                else:
                    embedVar = discord.Embed(title='Brawlhalla Profile', description=f'{profileStats}', color=0x008080)
                    await ctx.channel.send(embed=embedVar)

    @commands.command()
    async def brawl(self, ctx, parameter=None):
        mention = ctx.author.mention

        if not parameter == 'help':
            embedVar = discord.Embed(description=f'That is not a valid command, use \'$brawl help\' for a list of commands regarding Brawlhalla {mention}', color=0x008080)
            await ctx.channel.send(embed=embedVar)
        else:
            embedVar = discord.Embed(title='Brawlhalla Help', description=f'The bot contains various commands that allows the user to look at the legends, weapons, and personal profiles in Brawlhalla', color=0x008080)
            embedVar.add_field(name='$brawlLegend \'legend Name\'', value='This brings up the information of the legend entered by the user', inline=False)
            embedVar.add_field(name='$brawlWeaponSearch \'weapon1 weapon2\'', value='Weapon1 is a required input while weapon2 is optional, this will display all legends that wield the weapons inputted', inline=False)
            embedVar.add_field(name='$brawlProfile \'Brawlhalla ID\'', value='This will search up the Brawlhalla profile of the inputted ID displaying various profile information', inline=False)
            await ctx.channel.send(embed=embedVar)

# Sets up the bot commands above
def setup(bot):
    bot.add_cog(brawlhallaCommands(bot))
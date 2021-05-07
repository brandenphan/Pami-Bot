import os
import json
import random
import requests

import discord
from discord.ext import commands, tasks
from discord.ext.commands import CommandNotFound

import youtube_dl
from gtts import gTTS

from googlesearch import search
import wikipedia
import html

from pycoingecko import CoinGeckoAPI
import yfinance as yf

import re
import pymongo


# Imports the environment variables from discordTokens.env
from dotenv import load_dotenv
load_dotenv("discordTokens.env")
DISCORD_TOKEN = os.getenv("discord_token") 
DATABASE_LOGIN = os.getenv("database_login")
BRAWLHALLA_KEY = os.getenv("brawlhalla_key")

bot = commands.Bot(command_prefix='$')

@bot.event  # Event when the bot is logged in
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


# Help menu, showing all the commands the user can call from the bot
bot.remove_command('help')
@bot.command(pass_context=True)
async def help(ctx):
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


# Holds various commands involving the $todo functionality
@bot.command(pass_context=True)
async def todo(ctx):
    mention = ctx.author.mention

    # Shows an embedded message of everything on the to-do list
    if len(ctx.message.content) == 5:
        myClient = pymongo.MongoClient(f"{DATABASE_LOGIN}")
        listDatabase = myClient['todolist']
        personalTodoCollection = listDatabase[f'{ctx.author}']
        userData = personalTodoCollection.find({})

        dataString = ""
        numberDocuments = 0
        for data in userData:
            value = data['item']
            dataString += f'- {value}\n'
            numberDocuments += 1

        if numberDocuments == 0:
            dataString = 'Nothing on your to-do list'

        myClient.close()
        embedVar = discord.Embed(title='To-do List', description=f'{mention}\n\n{dataString}', color=0x3e7ada)
        await ctx.channel.send(embed=embedVar)
    else:
        # Adds the users input to the collection in the database
        if ctx.message.content[6:].lower().startswith('add'):
            myClient = pymongo.MongoClient(f"{DATABASE_LOGIN}")
            listDatabase = myClient['todolist']
            personalTodoCollection = listDatabase[f'{ctx.author}']
            userData = personalTodoCollection.find({})

            newItem = {'item': ctx.message.content[10:]}
            itemExistFlag = 0
            for data in userData:
                value = data['item']
                if (ctx.message.content[10:].lower() == value.lower()):
                    itemExistFlag = 1

            if itemExistFlag == 1:
                embedVar = discord.Embed(description=f'\'{ctx.message.content[10:]}\' is already on your to-do list {mention}', color=0x3e7ada)
                await ctx.channel.send(embed=embedVar)
            else:
                personalTodoCollection.insert_one(newItem)
                embedVar = discord.Embed(description=f'\'{ctx.message.content[10:]}\' has been added to your to-do list {mention}', color=0x3e7ada)
                await ctx.channel.send(embed=embedVar)
            myClient.close()
        
        # Removes the users input from their to-do list in the database
        elif ctx.message.content[6:].lower().startswith('remove'):
            myClient = pymongo.MongoClient(f"{DATABASE_LOGIN}")
            listDatabase = myClient['todolist']
            personalTodoCollection = listDatabase[f'{ctx.author}']
            userData = personalTodoCollection.find({})

            itemExistFlag = 0
            for data in userData:
                value = data['item']
                if (ctx.message.content[13:].lower() == value.lower()):
                    itemExistFlag = 1
            
            if itemExistFlag == 1:
                newItem = {'item': re.compile(ctx.message.content[13:], re.IGNORECASE)}
                personalTodoCollection.delete_one(newItem)
                embedVar = discord.Embed(description=f'\'{ctx.message.content[13:]}\' has been removed from your to-do list {mention}', color=0x3e7ada)
                await ctx.channel.send(embed=embedVar)
            else:
                embedVar = discord.Embed(description=f'\'{ctx.message.content[13:]}\' is not on your to-do list {mention}', color=0x3e7ada)
                await ctx.channel.send(embed=embedVar)
            myClient.close()

        # Removes all items on the users to-do list in the database
        elif ctx.message.content[6:].lower().startswith('reset'):
            myClient = pymongo.MongoClient(f"{DATABASE_LOGIN}")
            listDatabase = myClient['todolist']
            personalTodoCollection = listDatabase[f'{ctx.author}']
            personalTodoCollection.delete_many({})
            myClient.close()
            embedVar = discord.Embed(description=f'Your to-do list has been reset {mention}', color=0x3e7ada)
            await ctx.channel.send(embed=embedVar)

        # Help menu for the $todo commands
        elif ctx.message.content[6:].lower().startswith('help'):
            embedVar = discord.Embed(title='To-do List Help', description='$todo contains various commands to add and remove from your personal to-do list', color=0x3e7ada)
            embedVar.add_field(name='$todo', value='This will bring up your current to-do list', inline=False)
            embedVar.add_field(name='$todo add \'something\'', value='This will add \'something\' to your personal to-do list', inline=False)
            embedVar.add_field(name='$todo remove \'something\'', value='This will remove \'something\' from your personal to-do list', inline=False)
            embedVar.add_field(name='$todo reset', value='This will reset your to-do list', inline=False)
            await ctx.channel.send(embed=embedVar)

        # User inputs invalid command involving $todo
        else: 
            embedVar = discord.Embed(description=f'That is not a command, use \'$todo help\' to see the list of commands', color=0x3e7ada)
            await ctx.channel.send(embed=embedVar)


# Uses the yahoo finance to search for the stock entered by the user returning various information
@bot.command(pass_context=True)
async def stock(ctx):   
    mention = ctx.author.mention

    if len(ctx.message.content[7:]) == 0:
        embedVar=discord.Embed(description=f'Can\'t have an empty stock name {mention}', color=0x3e7ada)
        await ctx.channel.send(embed=embedVar)  
    else:
        try:
            stockName = ctx.message.content[7:]
            stock = yf.Ticker(stockName)
            todaysData = stock.history(period='1d')
            fullStockName = stock.info['shortName']
            link = f'https://finance.yahoo.com/quote/{stockName}?p={stockName}'
            twoDayHistory = stock.history(period='2d')
            dayDifference = twoDayHistory['Close'][1] - twoDayHistory['Close'][0]
            if dayDifference >= 0:
                embedColor = 0x009b938
            else:
                embedColor = 0xFF0000
            embedVar = discord.Embed(title=fullStockName, description=f'Price: $' + '%.2f' % todaysData['Close'][0], color=embedColor, url=link)
            await ctx.channel.send(mention)
            await ctx.channel.send(embed=embedVar)
        except:
            embedVar = discord.Embed(title=f'**{stockName}**', description='Stock does not exist')
            await ctx.channel.send(mention)
            await ctx.channel.send(embed=embedVar)


# Uses the CoinGecko API to get the price of the cryptocurrency inputted by the user
@bot.command(pass_context=True)
async def crypto(ctx): 
    mention = ctx.author.mention

    if len(ctx.message.content[8:]) == 0:
        embedVar=discord.Embed(description=f'Can\'t have an empty coin name {mention}', color=0xFFFF00)
        await ctx.channel.send(embed=embedVar)
    else:
        try:
            cg = CoinGeckoAPI()
            coinName = ctx.message.content[8:]
            coinPrice = cg.get_price(ids=coinName, vs_currencies='cad')
            embedVar = discord.Embed(title=f'**{coinName}**', description=f'Price: $' + '%.4f' % coinPrice[coinName]['cad'], color=0xFFFF00)
            await ctx.channel.send(mention)
            await ctx.channel.send(embed=embedVar)
        except:
            embedVar = discord.Embed(title=f'**{coinName}**', description='Coin does not exist')
            await ctx.channel.send(mention)
            await ctx.channel.send(embed=embedVar)


# Uses the search library to google search for the users input, retrieving the first link
@bot.command(pass_context=True)
async def google(ctx):  
    mention = ctx.author.mention

    if len(ctx.message.content[8:]) == 0:
        embedVar = discord.Embed(description=f'Cannot enter nothing to google search for {mention}', color=0x3e7ada)
        await ctx.channel.send(embed=embedVar)
    else:
        searchContent = ctx.message.content[8:]
        embedVar = discord.Embed(description=f'{mention} searched for {searchContent}', color=0x3e7ada)
        await ctx.channel.send(embed=embedVar)
        for i in search(searchContent, tld='co.in', num=1, stop=1, pause=2):
            await ctx.channel.send(i)


# Uses the wikipedia library to search for the users input on wikipedia grabbing the first section of the wikipedia page
@bot.command(pass_context=True)
async def wiki(ctx):   
    mention = ctx.author.mention

    if len(ctx.message.content[6:]) == 0:
        embedVar = discord.Embed(description=f'Cannot enter nothing to search for in wikipedia {mention}', color=0x808080)
        await ctx.channel.send(embed=embedVar)
    else:
        try:
            wikiSummary = wikipedia.summary(ctx.message.content[6:])

            # If the wikiSummary is less than 2000, puts it in a single embed, otherwise splits the wikiSummary into multiple embeds as the embed description limit is 2048
            if len(wikiSummary) <= 1900:
                embedVar = discord.Embed(description=f'{mention} searched for {ctx.message.content[6:]} on wikipedia\n\n{wikiSummary}', color=0x808080)
                await ctx.channel.send(embed=embedVar)
            else:
                embedList = []
                n = 1900
                embedList = [wikiSummary[i:i+n] for i in range(0, len(wikiSummary), n)]
                for index, embedInfo in enumerate(embedList, start = 1):
                    if index == 1:
                        embedVar = discord.Embed(description=f'{mention} searched for {ctx.message.content[6:]} on wikipedia\n\n{embedInfo}', color=0x808080)
                        await ctx.channel.send(embed=embedVar)
                    else:
                        embedVar = discord.Embed(description=embedInfo, color=0x808080)
                        await ctx.channel.send(embed=embedVar)
        except:
            embedVar = discord.Embed(description=f'{ctx.message.content[6:]} wikipedia page not found {mention}', color=0x808080)
            await ctx.channel.send(embed=embedVar)


# Flips a coin, displaying either heads or tails
@bot.command(pass_context=True)
async def flip(ctx):
    mention = ctx.author.mention
    flip = random.randint(0, 1)
    if (flip == 0):
        await ctx.channel.send(mention + ' `flips heads` ')
    else:
        await ctx.channel.send(mention + ' `flips tails` ')


# Rolls a die, displaying a number between 1 and 6
@bot.command(pass_context=True)
async def dice(ctx):
    mention = ctx.author.mention
    dice = random.randint(1,6)
    await ctx.channel.send(mention + f' `rolls {str(dice)}` ')


# Trivia game where a question will be displayed along with various information about the question, and the user can input an answer
@bot.command(pass_context=True)
async def trivia(ctx):
    mention = ctx.author.mention

    # Gets the JSON string text response from opent database
    response = requests.get('https://opentdb.com/api.php?amount=1')
    triviaResponse = json.loads(response.text)
    triviaResponseInformation = triviaResponse['results'][0]

    question = triviaResponseInformation['question']
    question = html.unescape(question)
    questionType = triviaResponseInformation['type']
    questionCategory = triviaResponseInformation['category']
    questionDifficulty = triviaResponseInformation['difficulty']
    questionAnswer = triviaResponseInformation['correct_answer']
    questionAnswer = html.unescape(questionAnswer)

    questionInformation = ""

    # Displays different formats for the answers depending on if the question is multiple choice or true or false
    if questionType == 'multiple':
        questionType = 'Multiple Choice'
        questionsArray = []

        # Gets all the possible answers in an array and randomizes the array
        questionsArray.append(triviaResponseInformation['correct_answer'])
        for incorrectQuestions in triviaResponseInformation['incorrect_answers']:
            decodedIncorrectQuestions = html.unescape(incorrectQuestions)
            questionsArray.append(decodedIncorrectQuestions)
        random.shuffle(questionsArray)

        individualQuestionsString = ""
        for individualQuestions in questionsArray:
            individualQuestionsString += f'{individualQuestions}\n' 

        questionInformation += f'Type: {questionType}\nCategory: {questionCategory}\nDifficulty: {questionDifficulty}\nQuestion: {question}\n\nAnswers: \n{individualQuestionsString}\nPlease type your answer in the chat:'
        embedVar = discord.Embed(title='Trivia', description=questionInformation, color=0xFFA500)
        await ctx.channel.send(embed=embedVar)

        # Ensures the author that initially started the trivia, is the one answering so other user messages aren't taken into account
        def check(m):
            return m.author == ctx.author

        # Gets the users answer and checks if the got the correct answer
        userAnswer = await bot.wait_for('message', check=check)
        if userAnswer.content.lower() == questionAnswer.lower():
            embedVar = discord.Embed(description=f'You chose the correct answer {mention}', color=0xFFA500)
            await ctx.channel.send(embed=embedVar)
        else:
            embedVar = discord.Embed(description=f'You chose the incorrect answer, the correct answer was \'{questionAnswer}\' {mention}', color=0xFFA500)
            await ctx.channel.send(embed=embedVar)

    else:
        questionType = 'True or False'

        questionInformation += f'Type:{questionType}\nCategory: {questionCategory}\nDifficulty: {questionDifficulty}\nQuestion: {question}\n\nAnswers: \nTrue\nFalse\n\nPlease type your in the chat:'
        embedVar = discord.Embed(title='Trivia', description=questionInformation, color=0xFFA500)
        await ctx.channel.send(embed=embedVar)

        # Ensures the author that initially started the trivia, is the one answering so other user messages aren't taken into account
        def check(m):
            return m.author == ctx.author

        # Gets the users answer and checks if the answer is correct
        userAnswer = await bot.wait_for('message', check=check)
        if userAnswer.content.lower() == questionAnswer.lower():
            embedVar = discord.Embed(description=f'You chose the correct answer {mention}', color=0XFFA500)
            await ctx.channel.send(embed=embedVar)
        else:
            embedVar = discord.Embed(description=f'You chose the incorrect answer, the correct answer was \'{questionAnswer}\' {mention}', color=0xFFA500)
            await ctx.channel.send(embed=embedVar)


# Gets the bot to join the users current voice channel
@bot.command(pass_context=True)
async def join(ctx):
    mention = ctx.author.mention

    # Checks if the bot is already in the channel
    try:
        server = ctx.author.voice

        # Checks if the user is in the channel
        if server is None:
            raise TypeError
        else:
            await server.channel.connect()
    except TypeError:
        embedVar = discord.Embed(description=f'You must be in the channel {mention}', color=0x3e7ada)
        await ctx.channel.send(embed=embedVar)     
    except Exception as error:
        embedVar = discord.Embed(description=f'I am already in the channel {mention}', color=0x3e7ada)
        await ctx.channel.send(embed=embedVar)
    

# Gets the bot to leave the current voice channel
@bot.command(pass_context=True)
async def leave(ctx):
    mention = ctx.author.mention
    try:
        inChannelCheck = ctx.author.voice
        
        # Checks if the user is in the channel
        if inChannelCheck is None:
            raise ValueError
        else:
            server = ctx.guild.voice_client

            # Checks if the bot is in the channel
            if server is None:
                raise TypeError
            else:
                await server.disconnect()
    except TypeError:
        embedVar = discord.Embed(description=f'I am not in the channel {mention}', color=0x3e7ada)
        await ctx.channel.send(embed=embedVar)
    except ValueError:
        embedVar = discord.Embed(description=f'You must be in the channel {mention}', color=0x3e7ada)
        await ctx.channel.send(embed=embedVar)


# Gets the bot to play audio of the youtube link/key words from the user
@bot.command(pass_context=True)
async def play(ctx, *, url=None):
    mention = ctx.author.mention

    if url is None:
        embedVar = discord.Embed(description=f'A youtube link or key words is required for $play. $play \'link/key words\' {mention}', color=0x3e7ada)
        await ctx.channel.send(embed=embedVar)
    else:
        # Gets the bot to join the voice channel if it was not previously there
        try: 
            server = ctx.author.voice
            await server.channel.connect()
        except:
            pass
        try:
            inChannelCheck = ctx.author.voice

            # Checks if the user is in the channel
            if inChannelCheck is None:
                raise ValueError
            else:
                server = ctx.message.guild
                voiceChannel = server.voice_client

                YDL_OPTIONS = {'format':'best audio', 'noplaylist':'True'}
                FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
                ydl_opts = {'format': 'bestaudio'}

                # Checks if the user entered a url or key words
                if url[0:4] == 'http':
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        try:
                            info = ydl.extract_info(url, download=False)
                            URL = info['formats'][0]['url']
                        except:
                            embedVar = discord.Embed(description=f'Could\'nt play {songTitle} {mention}', color=0xe37ada)
                            await ctx.channel.send(embed=embedVar)
                else:
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        try:
                            info = ydl.extract_info(f'ytsearch:{url}', download=False)['entries'][0]
                            URL = info['formats'][0]['url']
                        except:
                            embedVar = discord.Embed(description=f'Could\'nt play {songTitle} {mention}', color=0xe37ada)
                            await ctx.channel.send(embed=embedVar)                          
                try:
                    # Checks if there is currently a song playing, adds to queue if so
                    if voiceChannel.is_playing():
                        songQueue.append(info)
                        songTitle = info['title']
                        embedVar = discord.Embed(description=f'{songTitle} has been queued {mention}', color=0x3e7ada)
                        await ctx.channel.send(embed=embedVar)
                    else:
                        try:
                            voiceChannel.play(discord.FFmpegOpusAudio(URL, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))
                            songTitle = info['title']
                            embedVar = discord.Embed(description=f'{mention} playing {songTitle}', color=0x3e7ada)
                            await ctx.channel.send(embed=embedVar)
                        except:
                            embedVar = discord.Embed(description=f'Could\'nt play {songTitle} {mention}', color=0xe37ada)
                            await ctx.channel.send(embed=embedVar)
                except:
                    embedVar = discord.Embed(description=f'I am not in the channel {mention}', color=0x3e7ada)
                    await ctx.channel.send(embed=embedVar)
        except ValueError:
            embedVar = discord.Embed(description=f'You must be in the channel {mention}', color=0x3e7ada)
            await ctx.channel.send(embed=embedVar)


# Function to hold a music queue and play music until the queue is empty
songQueue = []
def play_next(ctx):
    server = ctx.message.guild
    voiceChannel = server.voice_client
    
    if len(songQueue) != 0 and not voiceChannel.is_playing():
        mention = ctx.author.mention
        server = ctx.message.guild
        voiceChannel = server.voice_client

        info = songQueue.pop(0)
        URL = info['formats'][0]['url']
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        voiceChannel.play(discord.FFmpegOpusAudio(URL, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))


# Gets the bot to stop the current song playing
@bot.command(pass_context=True)
async def stop(ctx):
    mention = ctx.author.mention

    try:
        inChannelCheck = ctx.author.voice

        # Checks if the user is in the channel
        if inChannelCheck is None:
            raise ValueError
        else:
            server = ctx.message.guild
            voiceChannel = server.voice_client

            # Checks if the bot is in the channel
            if voiceChannel is None:
                raise TypeError
            else:
                if voiceChannel.is_playing():
                    voiceChannel.stop()
                    songQueue.clear()
                    embedVar = discord.Embed(description=f'Stopping song {mention}', color=0x3e7ada)
                    await ctx.channel.send(embed=embedVar)
                else:
                    embedVar = discord.Embed(description=f'No song playing {mention}', color=0x3e7ada)
                    await ctx.channel.send(embed=embedVar)
    except ValueError:
        embedVar = discord.Embed(description=f'You must be in the channel {mention}', color=0x3e7ada)
        await ctx.channel.send(embed=embedVar)
    except TypeError:
        embedVar = discord.Embed(description=f'I am not in the channel {mention}', color=0x3e7ada)
        await ctx.channel.send(embed=embedVar)


# Gets the bot to pause the current song
@bot.command(pass_context=True)
async def pause(ctx):
    mention = ctx.author.mention

    try:
        inChannelCheck = ctx.author.voice

        # Checks if the user is in the channel
        if inChannelCheck is None:
            raise ValueError
        else:
            server = ctx.message.guild
            voiceChannel = server.voice_client

            # Checks if the bot is in the channel
            if voiceChannel is None:
                raise TypeError
            else:
                if voiceChannel.is_playing():
                    voiceChannel.pause()
                    embedVar = discord.Embed(description=f'Pausing music {mention}', color=0x3e7ada)
                    await ctx.channel.send(embed=embedVar)
                else:
                    embedVar = discord.Embed(description=f'No song playing {mention}', color=0x3e7ada)
                    await ctx.channel.send(embed=embedVar)
    except ValueError:
        embedVar = discord.Embed(description=f'You must be in the channel {mention}', color=0x3e7ada)
        await ctx.channel.send(embed=embedVar)
    except TypeError:
        embedVar = discord.Embed(description=f'I am not in the channel {mention}', color=0x3e7ada)
        await ctx.channel.send(embed=embedVar)


# Gets the bot to resume the current song
@bot.command(pass_context=True)
async def resume(ctx):
    mention = ctx.author.mention
    server = ctx.message.guild
    voiceChannel = server.voice_client

    try:
        inChannelCheck = ctx.author.voice

        # Checks if the user is in the channel
        if inChannelCheck is None:
            raise ValueError
        else:
            server = ctx.message.guild
            voiceChannel = server.voice_client

            # Checks if the bot is in the channel
            if voiceChannel is None:
                raise TypeError
            else:
                # Tries to resume the music 
                try:
                    voiceChannel.resume()
                    embedVar = discord.Embed(description=f'Resuming music {mention}', color=0x3e7ada)
                    await ctx.channel.send(embed=embedVar)
                except:
                    embedVar = discord.Embed(description=f'No music to resume {mention}', color=0x3e7ada)
                    await ctx.channel.send(embed=embedVar)
    except ValueError:
        embedVar = discord.Embed(description=f'You must be in the channel {mention}', color=0x3e7ada)
        await ctx.channel.send(embed=embedVar)
    except TypeError:
        embedVar = discord.Embed(description=f'I am not in the channel {mention}', color=0x3e7ada)
        await ctx.channel.send(embed=embedVar)


# Gets the bot to the skip the curent song
@bot.command(pass_context=True)
async def skip(ctx):
    mention = ctx.author.mention

    try:
        inChannelCheck = ctx.author.voice

        # Checks if the user is in the channel
        if inChannelCheck is None:
            raise ValueError
        else:
            server = ctx.message.guild
            voiceChannel = server.voice_client

            # Checks if the bot is in the channel
            if voiceChannel is None:
                raise TypeError
            else:
                if voiceChannel.is_playing():
                    voiceChannel.stop()

                    # If the is a song in the queue, skips to that song
                    if len(songQueue) != 0:
                        info = songQueue.pop(0)
                        URL = info['formats'][0]['url']
                        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
                        voiceChannel.play(discord.FFmpegOpusAudio(URL, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))

                    embedVar = discord.Embed(description=f'Skipping song {mention}', color=0x3e7ada)
                    await ctx.channel.send(embed=embedVar)
                else:
                    embedVar = discord.Embed(description=f'No song playing {mention}', color=0x3e7ada)
                    await ctx.channel.send(embed=embedVar)
    except ValueError:
        embedVar = discord.Embed(description=f'You must be in the channel {mention}', color=0x3e7ada)
        await ctx.channel.send(embed=embedVar)
    except TypeError:
        embedVar = discord.Embed(description=f'I am not in the channel {mention}', color=0x3e7ada)
        await ctx.channel.send(embed=embedVar)         


# Displays the user the current songs in the music queue
@bot.command(pass_context=True)
async def queue(ctx):
    mention = ctx.author.mention

    songList = ""
    for song in songQueue:
        songName = song['title']
        songList += f'{songName}\n'

    embedVar = discord.Embed(description=f'Music Queue {mention}\n{songList}', color=0x3e7ada)
    await ctx.channel.send(embed=embedVar)


# Shows the music help menu
@bot.command(pass_context=True)
async def music(ctx, parameter=None):
    mention = ctx.author.mention

    if not parameter == 'help':
        embedVar = discord.Embed(description=f'That is not a valid command, use \'$music help\' for a list of commands regarding the bots music player {mention}', color=0XB22222)
        await ctx.channel.send(embed=embedVar)
    else:
        embedVar = discord.Embed(title='Music Help', description=f'The bot contains various commands to control the music player. The bot can play music from youtube with the song link or key words of a song', color=0XB22222)
        embedVar.add_field(name='$play \'link/key words\'', value='This will get the bot to play music in the bots current voice channel from the link or play the first song found when searching for the key words', inline=False)
        embedVar.add_field(name='$stop', value='This will stop the music bot from playing music and clears the music queue', inline=False)
        embedVar.add_field(name='$pause', value='This will pause the current song playing on the music player', inline=False)
        embedVar.add_field(name='$resume', value='This will resume the current song if it was previously paused', inline=False)
        embedVar.add_field(name='$skip', value='This will skip the current song and play the next song in the queue if there is one', inline=False)
        embedVar.add_field(name='$queue', value='This will bring up the current songs in the music queue', inline=False)
        await ctx.channel.send(embed=embedVar)


# Gets the bot to say a phrase entered by the user in the voice channel
@bot.command(pass_context=True)
async def say(ctx, *, phrase=None):
    mention = ctx.author.mention

    # Gets the bot to join the voice channel if it was not previously there
    try: 
        server = ctx.author.voice
        await server.channel.connect()
    except:
        pass

    if phrase is None:
        embedVar = discord.Embed(description=f'Can\'t have an empty phrase for me to say {mention}', color=0x3e7ada)
        await ctx.channel.send(embed=embedVar)
    else:
        tts = gTTS(phrase)
        tts.save('say.mp3')

        server = ctx.message.guild
        voiceChannel = server.voice_client

        if voiceChannel.is_playing():
            embedVar = discord.Embed(description=f'I can\'t say anything because I am already talking or music is playing {mention}', color=0x3e7ada)
            await ctx.channel.send(embed=embedVar)
        else:
            voiceChannel.play(discord.FFmpegOpusAudio('say.mp3'))


# Gets the tetrio information regarding the profile entered by the user
@bot.command(pass_context=True)
async def tetrioProfile(ctx, name=None):
    mention = ctx.author.mention

    if name is None:
        embedVar = discord.Embed(description=f'Can\'t search for an empty profile name', color=0x3e7ada)
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


# Gets the brawlhalla characters information specified by the user
@bot.command(pass_context=True)
async def brawlLegend(ctx, name=None):
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


# Gets a list of characters that use the weapons entered by the user
@bot.command(pass_context=True)
async def brawlWeaponSearch(ctx, weapon1=None, weapon2=None):
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


# Gets the brawlhalla profile stats based on the input from the user
@bot.command(pass_context=True)
async def brawlProfile(ctx, userID=None):
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
              

# Displays the brawlhalla help menu
@bot.command(pass_context=True)
async def brawl(ctx, parameter=None):
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
import discord
from discord.ext import commands, tasks

import re
import pymongo
import os

# Imports environment variables from discordTokens.env
from dotenv import load_dotenv
load_dotenv('../discordTokens.env')
DATABASE_LOGIN = os.getenv('database_login')

# Commands regarding the To-do list
class todoCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def todo(self, ctx):
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

# Sets up the bot commands above
def setup(bot):
    bot.add_cog(todoCommands(bot))
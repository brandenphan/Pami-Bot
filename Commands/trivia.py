import discord
from discord.ext import commands, tasks

import requests
import json
import html
import random

# Commands for Trivia game
class triviaCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def trivia(self, ctx):
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
            decodedCorrectAnswer = html.unescape(triviaResponseInformation['correct_answer'])
            questionsArray.append(decodedCorrectAnswer)
            for incorrectQuestions in triviaResponseInformation['incorrect_answers']:
                decodedIncorrectQuestions = html.unescape(incorrectQuestions)
                questionsArray.append(decodedIncorrectQuestions)
            random.shuffle(questionsArray)

            questionAlphabet = 97

            individualQuestionsString = ""
            for individualQuestions in questionsArray:
                individualQuestionsString += f'{chr(questionAlphabet)}) {individualQuestions}\n' 
                questionAlphabet = questionAlphabet + 1

            questionInformation += f'{mention}\n\nType: {questionType}\nCategory: {questionCategory}\nDifficulty: {questionDifficulty}\nQuestion: {question}\n\nAnswers: \n{individualQuestionsString}\nPlease type your answer(a/b/c/d) in the chat:'
            embedVar = discord.Embed(title='Trivia', description=questionInformation, color=0xFFA500)
            await ctx.channel.send(embed=embedVar)

            # Ensures the author that initially started the trivia, is the one answering so other user messages aren't taken into account and they answer with 'a', 'b', 'c' or 'd'
            def check(m):
                return m.author == ctx.author and (m.content.lower() == 'a' or m.content.lower() == 'b' or m.content.lower() == 'c' or m.content.lower() == 'd')

            # Gets the users answer based off their letter input
            userAnswer = await self.bot.wait_for('message', check=check)
            answerValue = questionsArray[ord(userAnswer.content.lower())-97]

            # Checks if the users answer is correct
            if answerValue.lower() == questionAnswer.lower():
                embedVar = discord.Embed(description=f'You chose the correct answer {mention}', color=0xFFA500)
                await ctx.channel.send(embed=embedVar)
            else:
                embedVar = discord.Embed(description=f'You chose the incorrect answer, the correct answer was \'{questionAnswer}\' {mention}', color=0xFFA500)
                await ctx.channel.send(embed=embedVar)

        else:
            questionType = 'True or False'

            questionInformation += f'{mention}\n\nType:{questionType}\nCategory: {questionCategory}\nDifficulty: {questionDifficulty}\nQuestion: {question}\n\nAnswers: \na) True\nb) False\n\nPlease type your answer(a/b) in the chat:'
            embedVar = discord.Embed(title='Trivia', description=questionInformation, color=0xFFA500)
            await ctx.channel.send(embed=embedVar)

            # Ensures the author that initially started the trivia, is the one answering so other user messages aren't taken into account
            def check(m):
                return m.author == ctx.author and (m.content.lower() == 'a' or m.content.lower() == 'b')

            # Gets the users answer 
            userAnswer = await self.bot.wait_for('message', check=check)

            # Converts the users alphabetical answer to True or False
            if userAnswer.content.lower() == 'a':
                userAnswer = "True"
            elif userAnswer.content.lower() == 'b':
                userAnswer = "False"

            # Checks if the users answers is correct
            if userAnswer.lower() == questionAnswer.lower():
                embedVar = discord.Embed(description=f'You chose the correct answer {mention}', color=0XFFA500)
                await ctx.channel.send(embed=embedVar)
            else:
                embedVar = discord.Embed(description=f'You chose the incorrect answer, the correct answer was \'{questionAnswer}\' {mention}', color=0xFFA500)
                await ctx.channel.send(embed=embedVar)

# Sets up the trivia bot command above
def setup(bot):
    bot.add_cog(triviaCommands(bot))
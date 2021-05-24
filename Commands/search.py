import discord
from discord.ext import commands, tasks

from googlesearch import search
import wikipedia

# Commands to google search and wiki search
class searchCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def google(self, ctx):  
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

    @commands.command()
    async def wiki(self, ctx):   
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

# Sets up the bot commands above
def setup(bot):
    bot.add_cog(searchCommands(bot))
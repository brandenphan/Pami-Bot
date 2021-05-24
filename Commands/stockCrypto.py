import discord
from discord.ext import commands, tasks

from pycoingecko import CoinGeckoAPI
import yfinance as yf

# Commands for Stocks and Cryptocurrency
class stockCryptoCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def stock(self, ctx):
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

    @commands.command()
    async def crypto(self, ctx):
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

# Sets up the above commands
def setup(bot):
    bot.add_cog(stockCryptoCommands(bot))
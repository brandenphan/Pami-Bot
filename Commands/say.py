import discord
from discord.ext import commands, tasks

from gtts import gTTS

# Command to get bot to say something in voice channel
class sayCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def say(self, ctx, *, phrase=None):
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
            tts.save('AudioFolder/say.mp3')

            server = ctx.message.guild
            voiceChannel = server.voice_client

            if voiceChannel.is_playing():
                embedVar = discord.Embed(description=f'I can\'t say anything because I am already talking or music is playing {mention}', color=0x3e7ada)
                await ctx.channel.send(embed=embedVar)
            else:
                voiceChannel.play(discord.FFmpegOpusAudio('AudioFolder/say.mp3'))
            
# Sets up the bot command above
def setup(bot):
    bot.add_cog(sayCommand(bot))
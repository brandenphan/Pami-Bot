import discord
from discord.ext import commands, tasks

import youtube_dl

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

# Commands to play music in the voice channel
class musicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
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
        
    @commands.command()
    async def leave(self, ctx):
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
    
    @commands.command()
    async def play(self, ctx, *, url=None):
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

                    # Checks if the user entered a youtube url or key words
                    if url.startswith('https://www.youtube'):
                        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                            try:
                                info = ydl.extract_info(url, download=False)
                                URL = info['formats'][0]['url']
                            except:
                                embedVar = discord.Embed(description=f'Could\'nt play {url} {mention}', color=0xe37ada)
                                await ctx.channel.send(embed=embedVar)
                    else:
                        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                            try:
                                info = ydl.extract_info(f'ytsearch:{url}', download=False)['entries'][0]
                                URL = info['formats'][0]['url']
                            except:
                                embedVar = discord.Embed(description=f'Could\'nt play song {mention}', color=0xe37ada)
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

    @commands.command()
    async def stop(self, ctx):
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
        
    @commands.command()
    async def pause(self, ctx):
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
        
    @commands.command()
    async def resume(self, ctx):
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

    @commands.command()
    async def skip(self, ctx):
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

    @commands.command()
    async def queue(self, ctx):
        mention = ctx.author.mention

        songList = ""
        for song in songQueue:
            songName = song['title']
            songList += f'{songName}\n'

        embedVar = discord.Embed(description=f'Music Queue {mention}\n{songList}', color=0x3e7ada)
        await ctx.channel.send(embed=embedVar)
    
    @commands.command()
    async def music(self, ctx, parameter=None):
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

# Sets up the bot commands above
def setup(bot):
    bot.add_cog(musicCommands(bot))

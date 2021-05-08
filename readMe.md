# Pami Bot

This is a Discord bot that is written in Python and is currently hosted on Heroku servers for 24/7 service of the bot. Discord.py is the primary library that gives the bot various features ranging from trivia games to playing music in Discord. The bot utilizes many libraries that are included in the requirements.txt. It also has a few keys found in the "discordTokens.env" file that must be collected by the user before running the bot. All the code is written in the pami.py file and calls on the discordTokens.env so those tokens must be filled out before running the program.

# requirements.txt

This Discord bot utilizes many libraries that are found in the requirements.txt file. Specific versions are included with all the libraries so the user knows which version to download in the event that there are major changes in later versions of the libraries. This program also requires the user to install the ffmpeg library to play audio and cannot be installed directly using "pip". Instructions on how to install the ffmpeg library is found at https://www.wikihow.com/Install-FFmpeg-on-Windows.

# discordTokens.env

"discord_token" requires the Discord bot token that is given through the Discord developer portal. Instructions on how to retrieve a Discord bot token can be found at https://realpython.com/how-to-make-a-discord-bot-python/.

"database_login" is required for the bots connection to your mongoDB database that will allow the user to store information regarding the to-do list functionality of the bot. This requires you to set up a mongoDB cluster on the MongoDB Atlas. Once creating a cluster, there will be a connection link given for the cluster.

"brawlhalla_key" is an API key required for the bots connection to the BrawlHalla API which is needed to access the Brawlhalla features. This can be done by requesting for a Brawlhalla API key from them.

The "discord_token" is required as it gives the program a connection to a Discord bot entity. The "database_login" and "brawlhalla_key" are not mandatory but if you choose to not include these, you must remove all commands that depend on these keys as well as the getenv code at the start of the program that looks for these keys.

# Commands

The Discord bot contains various commands that can be seen by typing $help in a chat with the bot.

![pami_help](https://user-images.githubusercontent.com/82501158/117412068-51042480-aee2-11eb-8420-15b981dc6072.png)

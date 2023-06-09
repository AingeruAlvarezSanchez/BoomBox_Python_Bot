from dotenv import load_dotenv
import os

import discord
from discord.ext import commands

import youtube_dl
from googleapiclient.discovery import build

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
YOUTUBE_TOKEN = os.getenv("YOUTUBE_TOKEN")

# Bot intents for reading and reacting to guild messages
intents = discord.Intents()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Youtube format options
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    'hls_prefer_native': True
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
youtube_service = build('youtube', 'v3', developerKey=YOUTUBE_TOKEN)
# Youtube format options

# Removes the default help text message from Discord.py
bot.remove_command('help')


# Help texts submodule
def get_help_message():
    return """```List of supported commands:

!help:
	- Shows this help message.

!search <song_name>:
	- Searches the given song name and asks the user for a choice.

!play <song_name/digit>:
	- Plays the given song based on !search command output.

!pause 
	- Pauses the current song.

!stop
	- Stops all songs.
!skip
	- Skips the current song.

!qeue <song_name/digit>:
	- Adds the given song to the playlist based on !search command output.

!volume <digit>:
	- Sets the Bot volume, the valid values range from [1 to 10].```"""


# Help texts submodule


# Bot event submodule here
@bot.event
async def on_guild_join(guild):
    welcome_channel = discord.utils.get(guild.text_channels, name="general")
    if welcome_channel is None:
        welcome_channel = discord.utils.get(guild.text_channels, type=discord.ChannelType.text)
    else:
        await welcome_channel.send(get_help_message())


@bot.event
async def on_ready():
    print(f'{bot.user.name} Boombox successfully Connected to Discord')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == '!help':
        await help_command(message.channel)
    elif message.content.startswith('!search '):
        song_name = ' '.join(message.content.split(' ')[1:])
        await search(message.channel, song_name, message)


# Bot event submodule here

# Bot command handler submodules here
@bot.command()
async def help_command(ctx):
    await ctx.send(get_help_message())


@bot.command()
async def search(ctx, song_name, message):
    request = youtube_service.search().list(
        part='id,snippet',
        q=song_name,
        type='video',
        videoDefinition='high',
        videoEmbeddable='true',
        maxResults=5
    )
    response = request.execute()

    results = []
    for item in response['items']:
        video_title = item['snippet']['title']
        video_url = f'https://www.youtube.com/watch?v={item["id"]["videoId"]}'
        results.append({'title': video_title, 'url': video_url})

    choose_song = ''
    for index, result in enumerate(results):
        choose_song += f'{index + 1} - {result["title"]}\n'
    await ctx.send(f'```{choose_song}```')
    await ctx.send("""```!play <digit>: Plays the selected song immediately.
!queue <digit>: Adds the selected song to the queue.```""")

    # queue or play command
    # if
    # queue or play command

    # I need to check if the author of the message sent to wait_for is the same as the author which wrote the message
    choice = await bot.wait_for('message', check=lambda msg: msg.author == msg.author and msg.channel == msg.channel)

    # all the code below goes on play function
    command = choice.content.split()
    if command[1].isnumeric():
        selection = int(choice.content.split()[1]) - 1
    else:
        if command[0] == "!play":
            await ctx.send("```The provided argument was not a number, use !play <digit> in order to choose a song. "
                           "ex: !play 3```")
            return
        elif command[0] == "!queue":
            await ctx.send("```The provided argument was not a number, use !queue <digit> in order to add a song to "
                           "the queue. ex: !queue 3```")
            return

        # debugging
    print(f'{choice.author.name}')
    # debugging

    await ctx.send(f'{results[selection]["title"]}')
    if choice.author.voice and choice.channel:
        voice_channel = choice.author.voice.channel
        await voice_channel.connect()
        # FFMPEG nightmare
        # ffmpeg install here
        source = discord.FFmpegOpusAudio(results[selection]["title"])
    # message.author.voice.channel.play(source)
    # FFMPEG nightmare
    else:
        print('error message, the author is not on a voice channel')


@bot.command(name='play')
async def play(ctx):
    print('play command')


@bot.command(name='pause')
async def pause(ctx):
    print('pause command')


@bot.command(name='stop')
async def stop(ctx):
    print('stop command')


@bot.command(name='skip')
async def skip(ctx):
    print('skip command')


@bot.command(name='qeue')
async def qeue(ctx):
    print('queue command')


@bot.command(name='volume')
async def volume(ctx):
    print('volume command')


# Bot command handler submodules here

bot.run(DISCORD_TOKEN)

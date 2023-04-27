import discord
from discord.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyOAuth

#Bot intents for reading and reacting to guild messages
intents = discord.Intents()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

#Spotify base submodule
scope = "app-remote-control"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="04543ac90b20492b95e231cbff44be1f", client_secret="6e093fcbbab94d22aff32f223db20229", redirect_uri="http://localhost", scope=scope))
#Spotify base submodule

#Removes the default help text message from Discord.py
bot.remove_command('help')

#Help texts submodule
def get_help_message():
	return """```List of supported commands:

!help:
	- Shows this help message.

!search <song_name>:
	- Searchs the given song name and asks the user for a choice.

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

!set volume <digit>:
	- Sets the Bot volume, the valid values range from [1 to 10].```"""
#Help texts submodule


#Bot event submodule here
@bot.event
async def on_guild_join(guild):
	welcome_channel = discord.utils.get(guild.text_channels, name="general")
	if welcome_channel is None:
		welcome_channel = discord.utils.get(guild.text_channels, type=discord.ChannelType.text)

	if welcome_channel is not None:
		await welcome_channel.send(get_help_message())
#Bot event submodule here

#debug
@bot.event
async def on_ready():
    print(f'{bot.user.name} GruvBox sucessfully Connected to Discord')

@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	if message.content == '!help':
		await help_command(message.channel)
	elif message.content.startswith('!search '):
		print('hello')
		song_name = ' '.join(message.content.split(' ')[1:])
		search_result = sp.search(q='track' + song_name, limit=5, type='track')
		#track_uri = search_result['tracks']['items'][0]['id']
		#playback_uri = sp._get_uri(track_uri)
		#voice_state = message.author.voice
		#if voice_state and voice_state.channel:
		#	await voice_state.channel.connect()
		#	device_id = voice_state.channel.id
		#	sp.start_playback(device_id=device_id, context_uri=None, uris=[track_uri], offset=None, position_ms=None)
			#await play(voice_client)
		#await message.channel.send(f'Now playing: {song_name}')

#Bot command handler submodules here
@bot.command()
async def help_command(ctx):
	await ctx.send(get_help_message())

@bot.command(name='play')
async def play(ctx):
   print('') 
#Bot command handler submodules here

#TODO Token must be on private env
TOKEN_DISCORD = "MTA5OTA0MzE3NjA1ODIwNDE3Mg.GFAFGs.cxIV5wMLYnWLpCWFFKYWHvMq7KftQUGEeEwXvs"
bot.run(TOKEN_DISCORD)
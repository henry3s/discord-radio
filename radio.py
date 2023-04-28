import discord
from discord.ext import commands
import asyncio
import ffmpeg
from looping_audio_source import LoopingAudioSource
from collections import deque

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

TOKEN = "<YOUR TOKEN HERE>"
MP3_FILE = "<PATH/TO/MP3"

FFMPEG_OPTIONS = {
    "options": "-vn", 
}

connection_tasks = {}

async def connect_and_play(voice_channel):
    try:
        print(f"Attempting to connect to voice channel: {voice_channel.name} ({voice_channel.id})")
        voice_client = await voice_channel.connect()
        print(f"Connected to voice channel: {voice_channel.name} ({voice_channel.id})")
        audio_source = LoopingAudioSource(MP3_FILE, **FFMPEG_OPTIONS)

        async def on_disconnect():
            nonlocal voice_client
            while voice_client.is_connected():
                await asyncio.sleep(1)
            print(f"Disconnected from voice channel: {voice_channel.name} ({voice_channel.id})")
            voice_client.stop()
            if voice_client and voice_client.is_connected():
                await voice_client.cleanup()

            # Reconnect if the bot is not in a voice channel in the same guild or still connecting
            if voice_channel.guild.voice_client is None or voice_channel.guild.voice_client.is_connecting():
                await connect_and_play(voice_channel)

        voice_client.play(audio_source)
        asyncio.create_task(on_disconnect())
    except Exception as e:
        print(f"Error connecting to voice channel: {e}")
        await asyncio.sleep(5)
        # Check if the bot is already connected to a voice channel in this server
        if voice_channel.guild.voice_client is not None:
            return
        await connect_and_play(voice_channel)
    finally:
        global connection_tasks
        connection_tasks.pop(voice_channel.guild.id, None)

@bot.event
async def on_voice_state_update(member, before, after):
    if member.guild_permissions.administrator:
        if before.channel is None and after.channel is not None:
            if after.channel.guild.voice_client is not None:
                return

            global connection_tasks
            if after.channel.guild.id not in connection_tasks:
                task = asyncio.create_task(connect_and_play(after.channel))
                connection_tasks[after.channel.guild.id] = task

bot.run(TOKEN)
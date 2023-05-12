# discord-radio
a discord bot for streaming constant mp3 files through ffmpeg
can work in multiple servers at once, follows admin when initially joining a server, then stores 
the channel/server id in a json file to automatically reconnect on script updates (adding new files etc)
PREREQUISITES

pycord, asyncio, ffmpeg 

```
pip install pycord asyncio ffmpeg 
```

you may already have them from installing python / other projects 

SETUP

refer to https://discord.com/developers/docs/getting-started for how to set up a bot

change <AUDIO1> and <YOUR TOKEN ID> to their respective inputs.

you will need to run on a server, i recommend using screen to keep the script running 24/7.

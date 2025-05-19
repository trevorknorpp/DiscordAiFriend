import discord
import openai
from gtts import gTTS
from discord import FFmpegPCMAudio
import asyncio

#pip install PyNaCl
#pip install discord.py
#pip install openai
#pip install gTTS
#pip install openai==0.28



#put in openai key and discord memberID
openai.api_key = ''
memberId = 1234

# Initialize Discord Client
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Required to get information about the members in the voice channel
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot is ready. Logged in as {client.user}')

    # Check if you (or a specified user) are in a voice channel
    for guild in client.guilds:  # Iterate through all the guilds (servers) the bot is in
        for member in guild.members:  # Check the members in the guild
            if member.id == memberId and member.voice:  # join my voice chat Discord user ID
                # Join the voice channel the user is in
                voice_channel = member.voice.channel
                vc = await voice_channel.connect()
                print(f"Joined {voice_channel}")
                return  # Exit after connecting to the voice channel

@client.event
async def on_message(message):
    #if message.author == client.user:
        #return

    # Get user input
    user_input = message.content


    # List all available models
    models = openai.Model.list()

    # Print the model IDs
    for model in models['data']:
        print(model['id'])
    
    
    
    # Generate response from OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}]
    )

    reply = response['choices'][0]['message']['content']

    # Send text reply
    await message.channel.send(reply)

    # Convert text to speech using gTTS
    tts = gTTS(text=reply, lang='en')
    tts.save("response.mp3")

    # Check if the user is in a voice channel
    if message.author.voice:
        voice_channel = message.author.voice.channel
        vc = await voice_channel.connect()

        # Play the audio file
        vc.play(FFmpegPCMAudio('response.mp3'))

        # Disconnect after the audio is played
        while vc.is_playing():
            await asyncio.sleep(1)
        await vc.disconnect()
    else:
        await message.channel.send("You are not in a voice channel.")

client.run('MTI5ODQwNTc5ODMyOTcxNjc0Ng.GTKElw.K_tVEI-0Cezji6hHIHGQZ5Q2xo-QQ09euzRsN8')
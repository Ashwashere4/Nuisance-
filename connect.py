
import os
import discord
import Token
import numpy as np
import Responses


client = discord.Client(intents=discord.Intents.all())

lastMessageAuthor = 0

@client.event
async def on_ready():
    print("Bot is Ready!")

@client.event
async def on_message(message):
    
    string = message.content
    lowerString = string.lower()

    if message.author == message.author.bot:
        return
    
    if message.author == client.user.bot:
        return
    
    if string.isupper() == True:
        await message.reply("Woah there buddy, you need to calm down!")

    if "fuck" in lowerString:
        await message.reply(Responses.fuckResponse())

    if "kill myself" in lowerString:
        await message.reply(Responses.killResponse())


Token.run(client)
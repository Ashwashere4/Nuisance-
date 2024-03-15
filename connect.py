
import os
import discord
from discord.commands import option
import Token
import Responses
import time

bot = discord.Bot(intents=discord.Intents.all())

messageIDs = []
highest_reaction_number = 0
highest_reaction = " "

@bot.event
async def on_ready():
    print("Bot is Ready!")

@bot.event
async def on_message(message):
    
    channelID = message.channel.id

    # 1051027505542340618 ash's chat
    # 1213639591353909290 idea's chat

    if message.author == message.author.bot:
        return
    
    if message.author == bot.user.bot:
        return
    
    if channelID == 1214650027482288168 :
        string = message.content

        if "idea" in (string.lower()):
            print(message.id)
            messageIDs.append(message.id)
            await message.add_reaction('❌')
            await message.add_reaction('✅')
            
@bot.slash_command()
@option("amount", 
        description = "Enter an amount in minutes",
        min_value = 1,
        default = 30,)

async def timer(
    ctx : discord.ApplicationContext,
    amount : int,
):
    await ctx.respond(f"Created a timer for {amount} minutes!")
    user = ctx.author.id
    time.sleep(amount)
    await ctx.send(f"Timer is done! <@{user}>")


@bot.slash_command()

async def recall(
    ctx: discord.ApplicationContext,):

    print(messageIDs[0])
    message = ctx.channel.fetch_message(messageIDs[0])

    for reaction in message.reactions: # iterate through every reaction in the message
        if (reaction.count-1) > highest_reaction_number:
        # (reaction.count-1) discounts the bot's reaction
            highest_reaction = reaction.emoji
            highest_reaction_count = reaction.count-1
    await ctx.send(f"{highest_reaction} wins with {highest_reaction_count} votes!")

bot.run(Token.getKey())
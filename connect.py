
import os
import discord
from discord import *
import gitIgnore.Token as Token
import time
from spotifyapi import sp, playlistID, playlist, spotifyPlaylist

bot = discord.Bot(intents=discord.Intents.all())
messageIDs = []
playlistSet = set()
highest_reaction_number = 0
highest_reaction = " "

# databaseUtil.exec_sql_file('songRecommendation.sql')
# databaseUtil.connect()

@bot.event
async def on_ready():
    for i in playlist["tracks"]["items"]:
        playlistSet.add(i['track']['id'])
    print("playlistSet Created!")
    print("Bot is Ready!")

@bot.event
async def on_message(message):
    
    channelID = message.channel.id

    # 1051027505542340618 ash's chat
    # 1213639591353909290 idea's chat
    # 1214650027482288168 test's chat

    if message.author == message.author.bot:
        return
    
    if message.author == bot.user.bot:
        return
    
    if channelID == 1216427171833188503 :
        string = message.content

        # if "idea" in (string.lower()):
        #     print(message.id)
        #     messageIDs.append(message.id)
        #     await message.add_reaction('❌')
        #     await message.add_reaction('✅')

        if "https://open" in string:
            messageParsed = string.split()

            for i in messageParsed:
                if "https://open" in i:
                    print(i)
                    track = sp.track(i)

                    if track['id'] not in playlistSet:
                        sp.playlist_add_items(playlistID, [i])
                        playlistSet.add(track['id'])
                        

@bot.slash_command()
async def refreshplaylist(ctx):

    playlistSet = set()

    for i in playlist["tracks"]["items"]:
        playlistSet.add(i['track']['id'])

    await ctx.respond("Refresh internal Playlist set!")

@bot.slash_command()
async def getplaylist(ctx):
    await ctx.respond("Here is the current song recommendation playlist: " + spotifyPlaylist)

    
@bot.slash_command()
async def ping(ctx):
    await ctx.respond(f"AUGHHHHHHHHHHHHHHHHH {bot.latency}")

# @bot.slash_command()
# @option("amount", 
#         description = "Enter an amount in minutes",
#         min_value = 1,
#         default = 30,)

# async def timer(
#     ctx : discord.ApplicationContext,
#     amount : int,
# ):
#     await ctx.respond(f"Created a timer for {amount} minutes!")
#     user = ctx.author.id
#     time.sleep(amount)
#     await ctx.send(f"Timer is done! <@{user}>")

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
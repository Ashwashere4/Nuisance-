
import os
import Responses
import discord
from discord import *
import gitIgnore.Token as Token
import time
from spotifyapi import sp, playlistID, playlist, spotifyPlaylist

bot = discord.Bot(intents=discord.Intents.all())
messageIDs = []
playlistSet = set()
message_to_user = {}

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

    # string = message.content
    # lowerString = string.lower()
    # if message.author == message.author.bot:
    #     return
    
    # if message.author == client.user.bot:
    #     return
    
    # if string.isupper() == True:
    #     await message.reply("Woah there buddy, you need to calm down!")
    # if "fuck" in lowerString:
    #     await message.reply(Responses.fuckResponse())
    # if "kill myself" in lowerString:
        # await message.reply(Responses.killResponse())

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

                if "https://open.spotify.com/track/" in i:
                    print(i)
                    track = sp.track(i)

                    if track['id'] not in playlistSet:
                        sp.playlist_add_items(playlistID, [i])
                        playlistSet.add(track['id'])
                        await message.add_reaction('✅')
                        await message.add_reaction('❌')

                        message_to_user[message.id] = (message.author.id, track['id'])


                    else:
                        await message.reply("Either the song is already in the playlist or something went wrong. Wake up Ash if the latter")

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    message = reaction.message

    if reaction.emoji == '❌':

        if message.id in message_to_user:
            original_user_id, track_id = message_to_user[message.id]

            if user.id == original_user_id:

                if track_id in playlistSet:
                    sp.playlist_remove_all_occurrences_of_items(playlistID, [track_id])
                    playlistSet.remove(track_id)

                    del message_to_user[message.id]

                    await message.channel.send(f"{user.mention}, the song has been removed from the playlist")

                else:
                    await message.channel.send(f"The song is no longer in the playlist")
            else:
                await reaction.remove(user)
                        

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
async def houserules(ctx):
    with open('houseRules.txt', 'r') as file:
        content = file.read()
    await ctx.respond(f"{content}")

@bot.slash_command()
async def refreshplaylist(ctx):

    playlistSet = set()

    for i in playlist["tracks"]["items"]:
        playlistSet.add(i['track']['id'])

    await ctx.respond("Refresh internal Playlist set!")

@bot.slash_command()
async def ping(ctx):
    await ctx.respond(f"AUGHHHHHHHHHHHHHHHHH {bot.latency}")


bot.run(Token.getKey())
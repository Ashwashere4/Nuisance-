
from collections import defaultdict
import os
import Responses
import discord
from discord import *
import gitIgnore.Token as Token
import time
from spotifyapi import sp, playlistID, playlist, spotifyPlaylist
from helperFunctions import save_data_to_json, load_data_from_json

bot = discord.Bot(intents=discord.Intents.all())
messageIDs = []
playlistSet = set()
message_to_user = {}
reaction_confirmations = defaultdict(set)
reaction_confirmationsNegative = defaultdict(set)
messageAfterReason = []

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
    

    # Ash's server ID: 1110542946660536383
    # Forbidden Sock ID: 1216427171833188503
    if channelID == 1110542946660536383 :
        # Load the existing song data
        song_data = load_data_from_json()
        string = message.content

        
        if "https://open" in string:
            messageParsed = string.split()

            for i in messageParsed:

                if "https://open.spotify.com/track/" in i:
                    track = sp.track(i)

                    if not any(song['track_id'] == track['id'] for song in song_data):
                    
                        # Extract the part of the message after "Reason:"
                        reason_message = "No reason posted yet"
                        if "reason:" in string.lower():
                            # Split message and get the part after "Reason:"
                            reason_message = string.split("reason:")[1].strip()
                            print(reason_message)
                    

                    # Temporarily store the track info before adding
                        message_to_user[message.id] = {
                            'user_id': message.author.id,
                            'track_id': track['id'],
                            'track_url': i,
                            'track_name': track['name'],
                            'artist': track['artists'][0]['name'],
                            'user_name': message.author.name,
                            'Reason': reason_message
                    }

                        await message.add_reaction('✅')
                        await message.add_reaction('❌')
                        await message.reply("Song being considered")

                    else:
                        await message.reply("Either the song is already in the playlist or something went wrong. Wake up Ash if the latter")

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    message = reaction.message
    song_data = load_data_from_json()


    if reaction.emoji == '✅' and message.id in message_to_user:
        track_info = message_to_user[message.id]

        # # # Prevent the author from confirming their own song
        # if user.id == track_info['user_id']:
        #     await reaction.message.channel.send(f"{user.mention}, you can't vote for your own song!")
        #     await reaction.remove(user)
        #     return

        # Add the reaction if it's not from the author
        reaction_confirmations[message.id].add(user.id)

        if len(reaction_confirmations[message.id]) >= 2:
            # Add the track to the playlist
            sp.playlist_add_items(playlistID, [track_info['track_url']])

            # Update JSON
            song_data.append({
                'track_name': track_info['track_name'],
                'artist': track_info['artist'],
                'user_id': track_info['user_id'],
                'track_id': track_info['track_id'],
                'user_name': track_info['user_name'],
                'Reason' : track_info['Reason']
            })

            save_data_to_json(song_data)

            await message.channel.send(f"{message.author.mention}, ✅ Added **{track_info['track_name']}** by **{track_info['artist']}** to the playlist!")

            # Clean up
            del message_to_user[message.id]
            del reaction_confirmations[message.id]

    if reaction.emoji == '❌':

        if message.id in message_to_user:

            # print(message_to_user[message.id]['user_name'])
            # original_user_id, track_id = message_to_user[message.id]
            original_user_id = message_to_user[message.id]['user_id']
            track_id = message_to_user[message.id]['track_id']

            reaction_confirmationsNegative[message.id].add(user.id)

            if len(reaction_confirmationsNegative[message.id]) >= 2:

                # Load the current song data
                song_data = load_data_from_json()

                if any(song['track_id'] for song in song_data):
                    # Remove the track from the playlist
                    sp.playlist_remove_all_occurrences_of_items(playlistID, [track_id])

                    # Remove the song from the JSON data
                    song_data = [song for song in song_data if song['track_id'] != track_id]

                    # Save the updated data back to the JSON file
                    save_data_to_json(song_data)

                    del message_to_user[message.id]

                    await message.channel.send(f"{message.author.mention}, the song has been removed from consideration")

                else:
                    await message.channel.send(f"The song is no longer in the playlist")
            
    
@bot.slash_command()
async def getplaylist(ctx):
    await ctx.respond("Here is the current song recommendation playlist: " + spotifyPlaylist)

@bot.slash_command()
async def listplaylist(ctx):
    song_data = load_data_from_json()

    if not song_data:
        await ctx.respond("🎶 The playlist is currently empty!")
        return

    # Build a list of formatted lines
    formatted_entries = [
        f"**{song['track_name']}** by *{song['artist']}* — added by **{song['user_name']}** \n *Reason*: {song['Reason']}"
        for song in song_data
    ]

    output = "\n".join(formatted_entries)

    # Split into chunks if message is too long
    if len(output) > 2000:
        for chunk in [output[i:i+1900] for i in range(0, len(output), 1900)]:
            await ctx.respond(chunk)
    else:
        await ctx.respond(output)

@bot.slash_command()
async def houserules(ctx):
    with open('houseRules.txt', 'r') as file:
        content = file.read()
    await ctx.respond(f"{content}")

@bot.slash_command()
async def ping(ctx):
    await ctx.respond(f"AUGHHHHHHHHHHHHHHHHH {bot.latency}")

bot.run(Token.getKey())
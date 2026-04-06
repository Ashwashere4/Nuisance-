
from collections import defaultdict
import discord
from app_token import TOKEN
from collections import Counter
import json
from spotifyapi import sp, playlistID, playlist, spotifyPlaylist
from helperFunctions import save_data_to_json, load_data_from_json

bot = discord.Bot(intents=discord.Intents.all())
messageIDs = []
playlistSet = set()
message_to_user = {}
reaction_confirmations = defaultdict(set)
reaction_confirmationsNegative = defaultdict(set)
messageAfterReason = []
noSubmitList = []

# databaseUtil.exec_sql_file('songRecommendation.sql')
# databaseUtil.connect()

@bot.event
async def on_ready():
    print("Bot is Ready!")

def get_artist_genres(artist_name):
    # Search for the artist by name
    result = sp.search(q='artist:' + artist_name, type='artist', limit=1)
    if result['artists']['items']:
        artist = result['artists']['items'][0]
        return artist['genres']
    return []


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
    if channelID == 1216427171833188503 :
        # Load the existing song data
        song_data = load_data_from_json()
        string = message.content

        
        if "https://open" in string:
            messageParsed = string.split()

            # Check if the user is in the noSubmitList
            if message.author.name in noSubmitList:
                await message.reply("You are on the do not submit list and cannot submit songs.")
                return

            for i in messageParsed:

                if "https://open.spotify.com/track/" in i:
                    track = sp.track(i)

                    if not any(song['track_id'] == track['id'] for song in song_data):
                    
                        # Extract the part of the message after "Reason:"
                        reason_message = "No reason posted yet"
                        if "reason:" in string.lower():
                        # Find the position of 'reason:', and get the part after it
                            reason_index = string.lower().find("reason:")
                            reason_message = string[reason_index + len("reason:"):].strip()
                    

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
    track_info = message_to_user[message.id]

    if reaction.emoji == '✅' and message.id in message_to_user:

        # # # Prevent the author from confirming their own song
        if user.id == track_info['user_id']:
            await reaction.message.channel.send(f"{user.mention}, you can't vote for your own song!")
            await reaction.remove(user)
            return

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

            # Add the author of the song to the noSubmitList
            noSubmitList.append(track_info['user_name'])

            # If the length of noSubmitList exceeds 2, pop the first element
            if len(noSubmitList) > 2:
                freedom = noSubmitList.pop(0)
                await message.channel.send(f"{freedom.author.mention}, you are released from your shackles")

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

            # print (user.id == track_info['user_id'])
            if len(reaction_confirmationsNegative[message.id]) >= 2 or user.id == track_info['user_id']:

                await message.channel.send(f"{message.author.mention}, the song has been removed from consideration")

            
    
@bot.slash_command()
async def getplaylist(ctx):
    await ctx.respond("Here is the current song recommendation playlist: " + spotifyPlaylist)

@bot.slash_command()
async def getnolist(ctx):
    await ctx.respond(f"Here are the people in gay baby jail: {noSubmitList}")

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
async def distribution(ctx):
    # Load data from JSON file
    with open('songs_data.json', 'r') as f:
        data = json.load(f)
    
    # List to store the genres
    all_genres = []

    # Loop through each track in the data
    for entry in data:
        artist = entry["artist"]
        genres = get_artist_genres(artist)
        if genres:
            all_genres.extend(genres)

    # Count the frequency of each genre
    genre_count = Counter(all_genres)

    # Prepare the message to be sent
    genre_message = ""
    for genre, count in genre_count.items():
        genre_message += f"{genre}: {count} songs\n"

    # Send the genre distribution message
    if genre_message:
        await ctx.send(genre_message)
    else:
        await ctx.send("No genres found.")

@bot.slash_command(name="shutdown", description="Safely disconnects the bot and stops the script")
async def shutdown(ctx):
    # Security check: Only the owner can run this
    if ctx.author.id == 123456789012345678: # Replace with your Discord ID
        await ctx.respond("Shutting down...", ephemeral=True)
        
        print(f"Shutdown command received from {ctx.author}")
        
        # This closes the connection to Discord gateway and the aiohttp session
        await bot.close() 
    else:
        await ctx.respond("Permission denied. Only the bot owner can use this command.", ephemeral=True)

@bot.slash_command()
async def ping(ctx):
    await ctx.respond(f"AUGHHHHHHHHHHHHHHHHH {bot.latency}")

bot.run(TOKEN)
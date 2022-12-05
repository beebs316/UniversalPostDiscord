import tweepy, discord
from discord.ext import commands
import requests
import shutil

# twitter keys
api_key = ''
api_secret_key = ''
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

# Post discord
client = commands.Bot(command_prefix="!")
messages = []
sheetMessages = []
images = []
filenames = []


@client.event
async def on_message(message):
    channelIDsToListen = []  # put the channels that you want to listen to here
    if message.channel.id in channelIDsToListen:
        if message.content != "!twitter" and message.content != "!discordpost" and message.content != "!done":
            # append message
            if message.content != "":
                messages.append(message.content)

            imagesLen = len(message.attachments)

            # append image url
            if imagesLen > 0:
                images.append(message.attachments[0].url)
                filename = images[0].split('/')[-1]
                filenames.append(filename)
                r = requests.get(images[0], stream=True)
                if r.status_code == 200:
                    with open(filename, 'wb') as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)

    channelIDsToListen1 = []  # put the channels that you want to listen to here
    if message.channel.id in channelIDsToListen1:
        if message.content != "!twitter" and message.content != "!discordpost" and message.content != "!done":
            # append message
            if message.content != "":
                sheetMessages.append(message.content)

            imagesLen = len(message.attachments)

            # append image url
            if imagesLen > 0:
                images.append(message.attachments[0].url)
                filename = images[0].split('/')[-1]
                filenames.append(filename)
                r = requests.get(images[0], stream=True)
                if r.status_code == 200:
                    with open(filename, 'wb') as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)
    await client.process_commands(message)

#posting to twitter
@client.command()
async def twitterpost(ctx):
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)

    # Create API object
    api = tweepy.API(auth)

    # Upload image
    imageLen = len(images)
    textLen = len(messages)

    if imageLen > 0:
        media = api.media_upload(filenames[0])

    if textLen > 0 and imageLen > 0:
        # Post tweet text + image
        print("Post tweet text and image")
        r = api.update_status(status=messages[0], media_ids=[media.media_id])

    if textLen > 0 and imageLen == 0:
        # Post tweet text
        print("Post tweet text only")
        r = api.update_status(status=messages[0])

    if textLen == 0 and imageLen > 0:
        # Post tweet image
        print("Post tweet image only")
        r = api.update_status(status="", media_ids=[media.media_id])


@client.command()
async def discordpost(ctx):
    channel = client.get_channel()

    # Upload image
    imageLen = len(images)
    textLen = len(messages)

    if textLen > 0 and imageLen > 0:
        # Post tweet text + image
        print("Post discord text and image")
        await channel.send(messages[0], file=discord.File(filenames[0]))

    if textLen > 0 and imageLen == 0:
        # Post tweet text
        print("Post discord text only")
        await channel.send(messages[0])

    if textLen == 0 and imageLen > 0:
        # Post tweet image
        print("Post discord image only")
        await channel.send(file=discord.File(filenames[0]))


# clear content in queue
@client.command()
async def done(ctx):
    messages.clear()
    images.clear()
    filenames.clear()
@client.command()
async def sheets(ctx):
    messages.clear()
    images.clear()


client.run('')
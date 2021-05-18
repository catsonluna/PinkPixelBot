import time

import discord
import discord.utils
import json

from pymongo import MongoClient
from discord.ext import commands


def getJSON(filePathAndName):
    with open(filePathAndName, 'r') as fp:
        return json.load(fp)


private = getJSON('./private.json')

BotToken = private.get("token")

MongoDBPass = private.get("MongoDBPPass")
MongoDBPass2 = private.get("MongoDBPass2")

HypixelAPIKey1 = private.get("HypixelAPIKey1")
HypixelAPIKey2 = private.get("HypixelAPIKey2")

TwitchSecret = private.get("TwitchClientSeacret")
TwitchID = private.get("TwitchClientID")

cluster = MongoClient(MongoDBPass)
db2 = cluster["HightLimitMod"]
db = cluster["PinkPixel"]

DHT = MongoClient(MongoDBPass2)
PinkStats = DHT['PinkStats']

start_time = time.time()

initial_extensions = [
    'cogs.helpCommand',
    'cogs.comparing',
    'cogs.admin',
    'cogs.errorHandler',
    'cogs.heightLimitMod',
    'cogs.listeners',
    'cogs.pinkStats'
]


async def get_prefix(bot, message):
    if bot.user.id == 756153198456340511:
        prefixes = ["pp>"]
    else:
        prefixes = ["pd>"]
    return commands.when_mentioned_or(*prefixes)(bot, message)


intents = discord.Intents.default()
intents.members = True  # Subscribe to the privileged members intent.

bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, intents=intents)
bot.remove_command("help")
guild_ids = [803046779657781328]

for extension in initial_extensions:
    bot.load_extension(extension)

bot.load_extension("jishaku")

@bot.event
async def on_ready():
    print(f'Y-you tu-urned mwe on successfully daddy uwu, im looking at')
    print(bot.cogs)
    print("Guilds im in:")
    print(len(bot.guilds))
    print("People im watching over:")
    print(len(bot.users))
    # channel = bot.get_channel(806995896298110977)
    # await channel.send(f"bot is back online")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('pp>help to get started'))


bot.run(BotToken, bot=True, reconnect=True)

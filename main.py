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

MongoDBPass = private.get("MongoDBPpass")

HypixelAPIKey1 = private.get("HypixelAPIKey1")
HypixelAPIKey2 = private.get("HypixelAPIKey2")

TwitchSecret = private.get("TwitchClientSeacret")
TwitchID = private.get("TwitchClientID")

cluster = MongoClient(MongoDBPass)
db = cluster["PinkPixel"]

initial_extensions = [
    'cogs.helpCommand',
    'cogs.comparing',
    'cogs.liveAlert',
    'cogs.hypixelOnlinePing',
    'cogs.admin',
    'cogs.errorHandler'
]


async def get_prefix(bot, message):
    prefixes = ["pd>"]
    return commands.when_mentioned_or(*prefixes)(bot, message)


bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True)
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
    #channel = bot.get_channel(806995896298110977)
    #await channel.send(f"bot is back online")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('pp>help to get started'))


bot.run(BotToken, bot=True, reconnect=True)

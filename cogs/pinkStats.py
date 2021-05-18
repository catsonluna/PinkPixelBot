import datetime
import secrets
import random

import aiohttp
import discord
from discord.ext import commands

from main import HypixelAPIKey1, PinkStats

keys = PinkStats['api_keys']
user = PinkStats['users']


class PinkStatsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["api", "key", "gen_key"])
    @commands.has_role("Beta Tester")
    async def api_key(self, ctx, name: str = None):
        if name is None:
            await ctx.send("You need to provide an IGN")
            return
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f'https://api.mojang.com/users/profiles/minecraft/{name}') as resp:
                playerAPI = await resp.json()
        if 'error' in playerAPI:
            await ctx.send("There was an error finding that username")
            return
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f'https://api.hypixel.net/player?key={HypixelAPIKey1}&uuid={playerAPI["id"]}') as resp:
                hypixelAPI = await resp.json()
        if hypixelAPI['success'] is False:
            await ctx.send("There was an error finding that username")
            return
        if 'socialMedia' not in hypixelAPI['player']:
            await ctx.send("Couldnt find social medias in your api, you need to have your discord connected in order "
                           "to verify")
            return
        if f"{ctx.author}" != hypixelAPI['player']['socialMedia']['links']['DISCORD']:
            await ctx.send("You are not that person")
            return
        if keys.find_one({"uuid": hypixelAPI['player']['uuid']}):
            await ctx.send("You already have an api key")
            return
        generated_key = secrets.token_urlsafe(random.randint(32, 64))
        keys.insert_one({"uuid": hypixelAPI['player']['uuid'], "api_key": generated_key, "discordID": ctx.author.id,
                         "Banned": False, "Ban Reason": None, "Registration Date":
                             {"date": datetime.date.today(),
                              "timestamp": datetime.datetime.now().timestamp()},
                        "warnings": {}, "": False})

        user.insert_one({"uuid": hypixelAPI['player']['uuid'], "Overall": {}, "Overtime": {}})
        user.update_one({"_id": 1}, {"$inc": {"users": + 1}})
        color = ctx.author.color
        embed = discord.Embed(title='PinkStats Api Key', colour=color, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Info:", value=f"Do `/pinkstats key APIKEY` to insert the api key in the minecraft "
                                            f"mod.\n "
                                            f" Note, abusing the api key can get it banned and you wont be able to"
                                            f" use the mod :)",
                        inline=False)
        embed.add_field(name="Key:", value=f"```{generated_key}```", inline=False)
        embed.add_field(name="Developer:", value="Pinkulu", inline=False)
        try:
            await ctx.author.send(embed=embed)
            await ctx.send("I have sent you the api key in dms")
        except:
            await ctx.send("I couldnt dm you, please enable your dms and do `pp>get_key` to get it send again")


def setup(bot):
    bot.add_cog(PinkStatsCog(bot))

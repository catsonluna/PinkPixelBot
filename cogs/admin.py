import asyncio
import datetime

import aiohttp
import discord
from discord.ext import commands
import secrets

from main import HypixelAPIKey1, DHTDB


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="unload_cog", description="Unloads a cog that is already loaded.", aliases=["unload"],
                      usage="<cog name>")
    async def unload_cog(self, ctx, cog_name: str = None):
        if ctx.author.id == 324553306682818561:
            self.bot.unload_extension(f"cogs.{cog_name}")
            await ctx.send(f"unloaded {cog_name}")
        else:
            await ctx.send(f"Sorry <@{ctx.author.id}>, you cant run this command")

    @commands.command(name="load_cog", description="loads a cog that is unloaded.", aliases=["load"],
                      usage="<cog name>")
    async def load_cog(self, ctx, cog_name: str = None):
        if ctx.author.id == 324553306682818561:
            self.bot.load_extension(f"cogs.{cog_name}")
            await ctx.send(f"loaded {cog_name}")
        else:
            await ctx.send(f"Sorry <@{ctx.author.id}>, you cant run this command")

    @commands.command(aliases=["api", "key", "gen_key"])
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
        if 'socialMedia' not in hypixelAPI['player']:
            await ctx.send("Couldnt find social medias in your api, you need to have your discord connected in order "
                           "to verify")
            return
        if ctx.author != hypixelAPI['player']['socialMedia']['DISCORD']:
            await ctx.send("You are not that person")
            return
        if name in DHTDB['API_KEYS']:
            pass
        generated_key = secrets.token_urlsafe(32)
        await ctx.send(generated_key)

def setup(bot):
    bot.add_cog(Admin(bot))

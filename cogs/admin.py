import asyncio
import datetime

import aiohttp
import discord
from discord.ext import commands, tasks
import secrets

from main import HypixelAPIKey1, DHTDB


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.update_stats.start()

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

    @commands.command()
    async def send_thing(self, ctx):
        if ctx.author.id == 324553306682818561:
            channel = self.bot.get_channel(841727592406974504)
            color = ctx.author.color
            embed = discord.Embed(title='PinkPixel Stats', colour=color, timestamp=datetime.datetime.utcnow())
            embed.add_field(name="People using the bot:", value=f"0", inline=False)
            embed.add_field(name="Guilds the bot is in:", value=f"0", inline=False)
            embed.add_field(name="Commands the bot has:", value=f"0", inline=False)
            embed.add_field(name="Cogs the bot is using:", value=f"0", inline=False)

            await channel.send(embed=embed)

    @tasks.loop(seconds=60)
    async def update_stats(self):
        await self.bot.wait_until_ready()
        if self.bot.user.id == 699940714405953536:
            channel = self.bot.get_channel(841727592406974504)
            message = await channel.fetch_message(841729456209002597)
            embed = discord.Embed(title='PinkDev Stats(inactive most of the time)', colour=discord.Colour.from_rgb(253, 185, 255),
                                  timestamp=datetime.datetime.utcnow())
            embed.add_field(name="People using the bot:", value=f"{len(self.bot.users)}", inline=False)
            embed.add_field(name="Guilds the bot is in:", value=f"{len(self.bot.guilds)}", inline=False)
            embed.add_field(name="Commands the bot has:", value=f"{len(self.bot.commands)}", inline=False)
            embed.add_field(name="Cogs the bot is using:", value=f"{len(self.bot.cogs)}", inline=False)

            await message.edit(embed=embed)


def setup(bot):
    bot.add_cog(Admin(bot))

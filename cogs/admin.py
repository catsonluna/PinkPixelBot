import asyncio
import datetime

import discord
from discord.ext import commands


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


def setup(bot):
    bot.add_cog(Admin(bot))

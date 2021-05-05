import asyncio
import datetime

import discord
from discord.ext import commands

from main import db2

bedwars = db2["BedWars"]
HLA = db2["HeightLimitApp"]


class HLM(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add_map(self, ctx, teams: str = None, map_name: str = None, limit: int = None):
        if ctx.author.id == 324553306682818561:
            if teams is None:
                await ctx.send("You need to specify how many teams the map has (8 or 4)")
                return
            if map_name is None:
                await ctx.send("You need to specify the map")
                return
            if limit is None:
                await ctx.send("You need to specify the Limit")
                return
            if teams == "8" or teams == "8teams" or teams == "8team":
                BWmap = bedwars.find_one({"MapName": map_name, "Mode": "solo/doubles"})
                if BWmap:
                    await ctx.send("The map alread exists")
                else:
                    bedwars.insert_one({"MapName": map_name,
                                        "Limit": limit,
                                        "Mode": "solo/doubles"})
                    await ctx.send("Map has been added")
            elif teams == "4" or teams == "4teams" or teams == "4team":
                BWmap = bedwars.find_one({"MapName": map_name, "Mode": "3v3v3v3/4v4v4v4"})
                if BWmap:
                    await ctx.send("The map alread exists")
                else:
                    bedwars.insert_one({"MapName": map_name,
                                        "Limit": limit,
                                        "Mode": "3v3v3v3/4v4v4v4"})
                    await ctx.send("Map has been added")
            else:
                await ctx.send("Invalid Mode")
        else:
            await ctx.send(f"Sorry <@{ctx.author.id}>, you cant run this command")

    @commands.command()
    async def remove_map(self, ctx, teams: str = None, map_name: str = None):
        if ctx.author.id == 324553306682818561:
            if teams is None:
                await ctx.send("You need to specify how many teams the map has (8 or 4)")
                return
            if map_name is None:
                await ctx.send("You need to specify the map")
                return
            if teams == "8" or teams == "8teams" or teams == "8team":
                BWmap = bedwars.find_one({"MapName": map_name, "Mode": "solo/doubles"})
                if BWmap:
                    bedwars.delete_one(BWmap)
                    await ctx.send(f"i have deleted {map_name}")
                else:
                    await ctx.send("I couldnt find that map, sorry")
            elif teams == "4" or teams == "4teams" or teams == "4team":
                BWmap = bedwars.find_one({"MapName": map_name, "Mode": "3v3v3v3/4v4v4v4"})
                if BWmap:
                    bedwars.delete_one(BWmap)
                    await ctx.send(f"i have deleted {map_name}")
                else:
                    await ctx.send("I couldnt find that map, sorry")
            else:
                await ctx.send("Invalid Mode")
        else:
            await ctx.send(f"Sorry <@{ctx.author.id}>, you cant run this command")

    @commands.command()
    async def find_map(self, ctx, teams: str = None, map_name: str = None):
        if teams is None:
            await ctx.send("You need to specify how many teams the map has (8 or 4)")
            return
        if map_name is None:
            await ctx.send("You need to specify the map")
            return
        if teams == "8" or teams == "8teams" or teams == "8team":
            BWmap = bedwars.find_one({"MapName": map_name, "Mode": "solo/doubles"})
            if BWmap:
                await ctx.send(f"Name: {BWmap['MapName']}"
                               f"\nLimit: {BWmap['Limit']}"
                               f"\nMode: {BWmap['Mode']}")
            else:
                await ctx.send("I couldnt find that map, sorry")
        elif teams == "4" or teams == "4teams" or teams == "4team":
            BWmap = bedwars.find_one({"MapName": map_name, "Mode": "3v3v3v3/4v4v4v4"})
            if BWmap:
                await ctx.send(f"Name: {BWmap['MapName']}"
                               f"\nLimit: {BWmap['Limit']}"
                               f"\nMode: {BWmap['Mode']}")
            else:
                await ctx.send("I couldnt find that map, sorry")
        else:
            await ctx.send("Invalid Mode")

    @commands.command()
    async def set_msg(self, ctx, msg: str = None):
        if ctx.author.id == 324553306682818561:
            if msg is None:
                await ctx.send("You need to specify the msg")
                return
            HLA.update_one({"_id": 1},
                           {"$set": {"announcement": msg}})
            await ctx.send(f"message has been set to {msg}")
        else:
            await ctx.send(f"Sorry <@{ctx.author.id}>, you cant run this command")


def setup(bot):
    bot.add_cog(HLM(bot))

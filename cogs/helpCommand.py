import asyncio
import datetime

import discord
from discord.ext import commands


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def help(self, ctx):
        color = ctx.author.color
        embed = discord.Embed(title='PinkBot help', colour=color, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Overall:", value=f"overall (for hypixel overall stats)", inline=False)
        embed.add_field(name="BedWars:", value="bedwars (overall bedwars stats) \n"
                                                   "bedwars_solo (solo bedwars stats) \n"
                                                   "bedwars_doubles (double bedwars stats) \n"
                                                   "bedwars_threes (3v3v3v3 bedwars stats) \n"
                                                   "bedwars_fours (4v4v4v4 bedwars stats)",
                            inline=False)
        embed.add_field(name="Duels:", value=f"duels (for duels stats)", inline=False)
        embed.add_field(name="Example:", value=f"`pp>compare overall pinkulu technoblade`", inline=False)
        embed.add_field(name="Comparing stats with somone else:", value="pp>compare gamemode player1 player2",
                            inline=False)
        embed.add_field(name="Developer:", value="Pinkulu", inline=False)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def invite(self, ctx):
        color = ctx.author.color
        embed = discord.Embed(title='PinkBot invite', colour=color, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Link:", value=f"https://discord.com/api/oauth2/authorize?client_id=756153198456340511"
                                            f"&permissions=8&scope=bot", inline=False)
        embed.add_field(name="Developer:", value="Pinkulu", inline=False)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def source(self, ctx):
        color = ctx.author.color
        embed = discord.Embed(title='PinkBot source code', colour=color, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Link:", value=f"https://github.com/pinkulu/PinkPixelBot", inline=False)
        embed.add_field(name="Developer:", value="Pinkulu", inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))

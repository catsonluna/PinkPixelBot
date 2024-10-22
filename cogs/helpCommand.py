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
        embed = discord.Embed(title='PinkPixel help', colour=color, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Overall:", value=f"overall (for hypixel overall stats)", inline=False)
        embed.add_field(name="BedWars:", value="bedwars (overall bedwars stats) \n"
                                               "bedwars_solo (solo bedwars stats) \n"
                                               "bedwars_doubles (double bedwars stats) \n"
                                               "bedwars_threes (3v3v3v3 bedwars stats) \n"
                                               "bedwars_fours (4v4v4v4 bedwars stats)",
                        inline=False)
        embed.add_field(name="Duels:", value=f"duels (for duels stats)", inline=False)
        embed.add_field(name="Skywars:", value=f"skywars (for skywars stats)", inline=False)
        embed.add_field(name="Pit:", value=f"pit (for pit stats)", inline=False)
        embed.add_field(name="Blitz:", value=f"blitz (for blitz stats)", inline=False)
        embed.add_field(name="Comparing stats with somone else:", value="pp>compare gamemode player1 player2",
                        inline=False)
        embed.add_field(name="Example:", value=f"`pp>compare overall pinkulu technoblade`", inline=False)
        embed.add_field(name="Guilds:", value=f"You can compare 2 hypixel guilds", inline=False)
        embed.add_field(name="Example:", value=f"`pp>compare_guilds rawr hypemc`", inline=False)
        embed.add_field(name="Discord:", value=f"`You can compare 2 discord users", inline=False)
        embed.add_field(name="Example:", value=f"`pp>compare_users @pinkulu#6260 324553306682818561`", inline=False)
        embed.add_field(name="Note:", value=f"You can either use their ID or @ing them\nAlso you dont need to provide "
                                            f"2 people, if you only provide 1, it will compare that person to you",
                        inline=False)
        embed.add_field(name="Extra", value="some extra commands", inline=False)
        embed.add_field(name="Invite:", value=f"do pp>invite to invite the bot", inline=False)
        embed.add_field(name="Discord Server:", value=f"do pp>discord to to join the server for the bot", inline=False)
        embed.add_field(name="Source:", value=f"do pp>source to look at the source code", inline=False)


        embed.add_field(name="Developer:", value="Pinkulu", inline=False)
        try:
            await ctx.send(embed=embed)
        except:
            try:
                await ctx.author.send(embed=embed)
                await ctx.send("I couldnt send it here, so i dmd you the help command")
            except:
                await ctx.send("I couldnt send the help commmand here or to your dms")

    @commands.command(pass_context=True)
    async def invite(self, ctx):
        color = ctx.author.color
        embed = discord.Embed(title='PinkPixel invite', colour=color, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Link:", value=f"https://discord.com/api/oauth2/authorize?client_id=756153198456340511"
                                            f"&permissions=8&scope=bot", inline=False)
        embed.add_field(name="Developer:", value="Pinkulu", inline=False)
        try:
            await ctx.send(embed=embed)
        except:
            try:
                await ctx.author.send(embed=embed)
                await ctx.send("I have sent you an invite link in dms")
            except:
                await ctx.send("I couldnt send an invite link here or in dms")

    @commands.command(pass_context=True)
    async def source(self, ctx):
        color = ctx.author.color
        embed = discord.Embed(title='PinkPixel source code', colour=color, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Link:", value=f"https://github.com/pinkulu/PinkPixelBot", inline=False)
        embed.add_field(name="Developer:", value="Pinkulu", inline=False)
        try:
            await ctx.send(embed=embed)
        except:
            try:
                await ctx.author.send(embed=embed)
                await ctx.send("i have sent the github link to your dms")
            except:
                await ctx.send("i couldnt send the github link here or to your dms")

    @commands.command(pass_context=True)
    async def discord(self, ctx):
        color = ctx.author.color
        embed = discord.Embed(title='PinkPixel Discord Server', colour=color, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Info:", value="Join the discord server to suggest features, report bugs, "
                                            "get help about the bot, or just talk", inline=False)
        embed.add_field(name="Link:", value=f"https://discord.gg/Fykpshg", inline=False)
        embed.add_field(name="Developer:", value="Pinkulu", inline=False)
        try:
            await ctx.send(embed=embed)
        except:
            try:
                await ctx.author.send(embed=embed)
                await ctx.send("i have sent the github link to your dms")
            except:
                await ctx.send("i couldnt send the github link here or to your dms")


def setup(bot):
    bot.add_cog(Help(bot))

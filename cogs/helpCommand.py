import asyncio
import datetime

import discord
from discord.ext import commands


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def help(self, ctx, help: str = None):
        color = ctx.author.color
        embed = discord.Embed(title='PinkBot help', colour=color, timestamp=datetime.datetime.utcnow())
        if help == "compare":
            embed.add_field(name="Overall:", value=f"overall (for hypixel overall stats)", inline=False)
            embed.add_field(name="BedWars:", value="bedwars (overall bedwars stats) \n"
                                                   "bedwars_solo (solo bedwars stats) \n"
                                                   "bedwars_doubles (double bedwars stats) \n"
                                                   "bedwars_threes (3v3v3v3 bedwars stats) \n"
                                                   "bedwars_fours (4v4v4v4 bedwars stats)",
                            inline=False)
            embed.add_field(name="Example:", value=f"`pp>compare overall pinkulu technoblade`", inline=False)
        else:
            embed.add_field(name="Hypixel Online Ping:",
                            value=f"pp>stalk username (pings you whenever the person your stalking gets online) \n"
                                  f"pp>un_stalk username (stops you from getting pinged)\n"
                                  f"pp>dm_toggle (toggles whether the bot dms you or pings you \n"
                                  f"pp>get_people (shows you all the people you are stalking)"
                                  f"pp>total_people (how many people are being stalked", inline=False)
            embed.add_field(name="Comparing stats with somone else:", value="pp>compare gamemode player1 player2 \n"
                                                                            "for all the available gamemodes do pp>help compare",
                            inline=False)
        embed.add_field(name="Developer:", value="Pinkulu", inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))

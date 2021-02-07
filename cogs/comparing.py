import asyncio
import datetime

import aiohttp
import discord
from discord.ext import commands


class Compare(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #change to hypixel API when i get my 3rd api key
    @commands.command(name="compare", description="Get hypixel stats")
    async def compare(self, ctx, gamemode: str = None, player1: str = None, player2: str = None):
        mode = gamemode.lower()
        if mode is None:
            await ctx.send("the format is: `pp>compare game player1 player2`")
            return
        if player1 is None:
            await ctx.send("the format is: `pp>compare game player1 player2`")
            return
        if player2 is None:
            await ctx.send("the format is: `pp>compare game player1 player2`")
            return
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.slothpixel.me/api/players/{player1}') as resp:
                player1API = await resp.json()
            async with session.get(f'https://api.slothpixel.me/api/players/{player2}') as resp:
                player2API = await resp.json()
        if 'error' in player1API:
            await ctx.send("Wrong Player1 Username")
            return
        if 'error' in player2API:
            await ctx.send("Wrong Player2 Username")
            return
        elif mode == "overall":
            if player1API['rank'] == "MVP_PLUS_PLUS":
                player1Rank = "MVP++"
            elif player1API['rank'] == "MVP_PLUS":
                player1Rank = "MVP+"
            elif player1API['rank'] == "VIP_PLUS":
                player1Rank = "VIP+"
            else:
                player1Rank = f"{player1API['rank']}"

            if player2API['rank'] == "MVP_PLUS_PLUS":
                player2Rank = "MVP++"
            elif player2API['rank'] == "MVP_PLUS":
                player2Rank = "MVP+"
            elif player2API['rank'] == "VIP_PLUS":
                player2Rank = "VIP+"
            else:
                player2Rank = f"{player2API['rank']}"

            if player1API['online']:
                player1OnlineStatus = "Online"
            else:
                player1OnlineStatus = "Offline"

            if player2API['online']:
                player2OnlineStatus = "Online"
            else:
                player2OnlineStatus = "Offline"

            color = ctx.author.color
            embed = discord.Embed(title=f'Overall stats: \n` {player1} ` vs ` {player2} `', colour=color,
                                  timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Level:", value=f"` {player1API['level']} ` vs ` {player2API['level']} `",
                            inline=False)
            embed.add_field(name="Rank:", value=f"` {player1Rank} ` vs ` {player2Rank} `", inline=False)
            embed.add_field(name="Karma:", value=f"` {player1API['karma']} ` vs ` {player2API['karma']} `",
                            inline=False)
            embed.add_field(name="Achievement Points:",
                            value=f"` {player1API['achievement_points']} ` vs ` {player2API['achievement_points']} `",
                            inline=False)
            embed.add_field(name="Last Game:", value=f"` {player1API['last_game']} ` vs ` {player2API['last_game']} `",
                            inline=False)
            embed.add_field(name="Online Status:", value=f"` {player1OnlineStatus} ` vs ` {player2OnlineStatus} `",
                            inline=False)

            await ctx.send(embed=embed)

        elif mode == "bedwars":
            color = ctx.author.color
            embed = discord.Embed(title=f'Overall BedWars stats: \n` {player1} ` vs ` {player2} `', colour=color,
                                  timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Star:",
                            value=f"` {player1API['stats']['BedWars']['level']} ` vs ` {player2API['stats']['BedWars']['level']} `",
                            inline=False)
            embed.add_field(name="Winstreak:",
                            value=f"` {player1API['stats']['BedWars']['winstreak']} ` vs ` {player2API['stats']['BedWars']['winstreak']} `",
                            inline=False)
            embed.add_field(name="FKDR:",
                            value=f"` {player1API['stats']['BedWars']['final_k_d']} ` vs ` {player2API['stats']['BedWars']['final_k_d']} `",
                            inline=False)
            embed.add_field(name="Final Kills:",
                            value=f"` {player1API['stats']['BedWars']['final_kills']} ` vs ` {player2API['stats']['BedWars']['final_kills']} `",
                            inline=False)
            embed.add_field(name="Final Deaths:",
                            value=f"` {player1API['stats']['BedWars']['final_deaths']} ` vs ` {player2API['stats']['BedWars']['final_deaths']} `",
                            inline=False)
            embed.add_field(name="Beds Destroyed:",
                            value=f"` {player1API['stats']['BedWars']['beds_broken']} ` vs ` {player2API['stats']['BedWars']['beds_broken']} `",
                            inline=False)
            embed.add_field(name="Games Played:",
                            value=f"` {player1API['stats']['BedWars']['games_played']} ` vs ` {player2API['stats']['BedWars']['games_played']} `",
                            inline=False)
            embed.add_field(name="Wins:",
                            value=f"` {player1API['stats']['BedWars']['wins']} ` vs ` {player2API['stats']['BedWars']['wins']} `",
                            inline=False)
            embed.add_field(name="Coins:",
                            value=f"` {player1API['stats']['BedWars']['coins']} ` vs ` {player2API['stats']['BedWars']['coins']} `",
                            inline=False)
            await ctx.send(embed=embed)

        elif mode == "bedwars_solo":
            color = ctx.author.color
            fkdr1 = player1API['stats']['BedWars']['gamemodes']['solo']['final_kills'] / \
                    player1API['stats']['BedWars']['gamemodes']['solo']['final_deaths']
            fkdr2 = player2API['stats']['BedWars']['gamemodes']['solo']['final_kills'] / \
                    player2API['stats']['BedWars']['gamemodes']['solo']['final_deaths']
            embed = discord.Embed(title=f'Solo BedWars stats: \n` {player1} ` vs ` {player2} `', colour=color,
                                  timestamp=datetime.datetime.utcnow())
            embed.add_field(name="FKDR:",
                            value=f"` %.2f `" % fkdr1 + " vs " + "` %.2f `" % fkdr2,
                            inline=False)
            embed.add_field(name="Final Kills:",
                            value=f"` {player1API['stats']['BedWars']['gamemodes']['solo']['final_kills']} ` vs ` {player2API['stats']['BedWars']['gamemodes']['solo']['final_kills']} `",
                            inline=False)
            embed.add_field(name="Final Deaths:",
                            value=f"` {player1API['stats']['BedWars']['gamemodes']['solo']['final_deaths']} ` vs ` {player2API['stats']['BedWars']['gamemodes']['solo']['final_deaths']} `",
                            inline=False)
            embed.add_field(name="Beds Broken:",
                            value=f"` {player1API['stats']['BedWars']['gamemodes']['solo']['beds_broken']} ` vs ` {player2API['stats']['BedWars']['gamemodes']['solo']['beds_broken']} `",
                            inline=False)
            embed.add_field(name="Wins:",
                            value=f"` {player1API['stats']['BedWars']['gamemodes']['solo']['wins']} ` vs ` {player2API['stats']['BedWars']['gamemodes']['solo']['wins']} `",
                            inline=False)
            embed.add_field(name="Losses:",
                            value=f"` {player1API['stats']['BedWars']['gamemodes']['solo']['losses']} ` vs ` {player2API['stats']['BedWars']['gamemodes']['solo']['losses']} `",
                            inline=False)
            embed.add_field(name="Winstreak:",
                            value=f"` {player1API['stats']['BedWars']['gamemodes']['solo']['winstreak']} ` vs ` {player2API['stats']['BedWars']['gamemodes']['solo']['winstreak']} `",
                            inline=False)
            await ctx.send(embed=embed)

        elif mode == "bedwars_doubles":
            color = ctx.author.color
            fkdr1 = player1API['stats']['BedWars']['gamemodes']['doubles']['final_kills'] / \
                    player1API['stats']['BedWars']['gamemodes']['doubles']['final_deaths']
            fkdr2 = player2API['stats']['BedWars']['gamemodes']['doubles']['final_kills'] / \
                    player2API['stats']['BedWars']['gamemodes']['doubles']['final_deaths']
            embed = discord.Embed(title=f'Doubles BedWars stats: \n` {player1} ` vs ` {player2} `', colour=color,
                                  timestamp=datetime.datetime.utcnow())
            embed.add_field(name="FKDR:",
                            value=f"` %.2f `" % fkdr1 + " vs " + "` %.2f `" % fkdr2,
                            inline=False)
            embed.add_field(name="Final Kills:",
                            value=f"` {player1API['stats']['BedWars']['gamemodes']['doubles']['final_kills']} ` vs ` {player2API['stats']['BedWars']['gamemodes']['doubles']['final_kills']} `",
                            inline=False)
            embed.add_field(name="Final Deaths:",
                            value=f"` {player1API['stats']['BedWars']['gamemodes']['doubles']['final_deaths']} ` vs ` {player2API['stats']['BedWars']['gamemodes']['doubles']['final_deaths']} `",
                            inline=False)
            embed.add_field(name="Beds Broken:",
                            value=f"` {player1API['stats']['BedWars']['gamemodes']['doubles']['beds_broken']} ` vs ` {player2API['stats']['BedWars']['gamemodes']['doubles']['beds_broken']} `",
                            inline=False)
            embed.add_field(name="Wins:",
                            value=f"` {player1API['stats']['BedWars']['gamemodes']['doubles']['wins']} ` vs ` {player2API['stats']['BedWars']['gamemodes']['doubles']['wins']} `",
                            inline=False)
            embed.add_field(name="Losses:",
                            value=f"` {player1API['stats']['BedWars']['gamemodes']['doubles']['losses']} ` vs ` {player2API['stats']['BedWars']['gamemodes']['doubles']['losses']} `",
                            inline=False)
            embed.add_field(name="Winstreak:",
                            value=f"` {player1API['stats']['BedWars']['gamemodes']['doubles']['winstreak']} ` vs ` {player2API['stats']['BedWars']['gamemodes']['doubles']['winstreak']} `",
                            inline=False)
            await ctx.send(embed=embed)

        elif mode == "bedwars_threes":
            color = ctx.author.color
            fkdr1 = player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_kills'] / \
                    player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_deaths']
            fkdr2 = player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_kills'] / \
                    player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_deaths']
            embed = discord.Embed(title=f'Threes BedWars stats: \n` {player1} ` vs ` {player2} `', colour=color,
                                  timestamp=datetime.datetime.utcnow())
            embed.add_field(name="FKDR:",
                            value=f"` %.2f `" % fkdr1 + " vs " + "` %.2f `" % fkdr2,
                            inline=False)
            embed.add_field(name="Final Kills:",
                            value=f"` {player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_kills']} ` vs ` {player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_kills']} `",
                            inline=False)
            embed.add_field(name="Final Deaths:",
                            value=f"` {player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_deaths']} ` vs ` {player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_deaths']} `",
                            inline=False)
            embed.add_field(name="Beds Broken:",
                            value=f"` {player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['beds_broken']} ` vs ` {player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['beds_broken']} `",
                            inline=False)
            embed.add_field(name="Wins:",
                            value=f"` {player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['wins']} ` vs ` {player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['wins']} `",
                            inline=False)
            embed.add_field(name="Losses:",
                            value=f"` {player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['losses']} ` vs ` {player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['losses']} `",
                            inline=False)
            embed.add_field(name="Winstreak:",
                            value=f"` {player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['winstreak']} ` vs ` {player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['winstreak']} `",
                            inline=False)
            await ctx.send(embed=embed)

        elif mode == "bedwars_fours":
            color = ctx.author.color
            fkdr1 = player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_kills'] / \
                    player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_deaths']
            fkdr2 = player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_kills'] / \
                    player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_deaths']
            embed = discord.Embed(title=f'Fours BedWars stats: \n` {player1} ` vs ` {player2} `', colour=color,
                                  timestamp=datetime.datetime.utcnow())
            embed.add_field(name="FKDR:",
                            value=f"` %.2f `" % fkdr1 + " vs " + "` %.2f `" % fkdr2,
                            inline=False)
            embed.add_field(name="Final Kills:",
                            value=f"` {player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_kills']} ` vs ` {player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_kills']} `",
                            inline=False)
            embed.add_field(name="Final Deaths:",
                            value=f"` {player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_deaths']} ` vs ` {player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_deaths']} `",
                            inline=False)
            embed.add_field(name="Beds Broken:",
                            value=f"` {player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['beds_broken']} ` vs ` {player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['beds_broken']} `",
                            inline=False)
            embed.add_field(name="Wins:",
                            value=f"` {player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['wins']} ` vs ` {player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['wins']} `",
                            inline=False)
            embed.add_field(name="Losses:",
                            value=f"` {player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['losses']} ` vs ` {player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['losses']} `",
                            inline=False)
            embed.add_field(name="Winstreak:",
                            value=f"` {player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['winstreak']} ` vs ` {player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['winstreak']} `",
                            inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("That gamemode is not valid")


def setup(bot):
    bot.add_cog(Compare(bot))

import asyncio
import datetime
import io

import aiohttp
import discord
import requests
from discord.ext import commands
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


class Compare(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.same = 130, 130, 130
        self.better = 70, 255, 70
        self.worse = 255, 92, 92
        self.neutral = 255, 255, 255

    # change to hypixel API when i get my 3rd api key
    @commands.command(name="compare", description="Get hypixel stats")
    async def compare(self, ctx, gamemode: str = None, player1: str = None, player2: str = None):
        if gamemode is None:
            await ctx.send("the format is: `pp>compare game player1 player2`")
            return
        mode = gamemode.lower()
        if player1 is None:
            await ctx.send("the format is: `pp>compare game player1 player2`")
            return
        if player2 is None:
            await ctx.send("the format is: `pp>compare game player1 player2`")
            return
        async with ctx.typing():
            color = ctx.author.color
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

                img = Image.open("infoimgimg.png")
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("Minecraftia.ttf",
                                          65)
                fontbig = ImageFont.truetype("Minecraftia.ttf",
                                             250)
                draw.text((0, 0), "Overall:", self.neutral, font=fontbig)

                draw.text((0, 400), f"Username:\n{player1}", self.neutral,
                          font=font)
                draw.text((1300, 400), f"Username:\n{player2}", self.neutral,
                          font=font)

                draw.text((0, 700), f"Rank: {player1Rank}", self.neutral,
                          font=font)
                draw.text((1300, 700), f"Rank: {player2Rank}", self.neutral,
                          font=font)
                if player1API['level'] > player2API['level']:
                    draw.text((0, 900), f"Level: {player1API['level']}", self.better,
                              font=font)
                    draw.text((1300, 900), f"Level: {player2API['level']}", self.worse,
                              font=font)
                elif player1API['level'] == player2API['level']:
                    draw.text((0, 900), f"Level: {player1API['level']}", self.same,
                              font=font)
                    draw.text((1300, 900), f"Level: {player2API['level']}", self.same,
                              font=font)
                else:
                    draw.text((0, 900), f"Level: {player1API['level']}", self.worse,
                              font=font)
                    draw.text((1300, 900), f"Level: {player2API['level']}", self.better,
                              font=font)

                if player1API['karma'] > player2API['karma']:
                    draw.text((0, 1100), "Karma: {:,}".format(player1API['karma']), self.better,
                              font=font)
                    draw.text((1300, 1100), "Karma: {:,}".format(player2API['karma']), self.worse,
                              font=font)
                elif player1API['karma'] == player2API['karma']:
                    draw.text((0, 1100), "Karma: {:,}".format(player1API['karma']), self.same,
                              font=font)
                    draw.text((1300, 1100), "Karma: {:,}".format(player2API['karma']), self.same,
                              font=font)
                else:
                    draw.text((0, 1100), "Karma: {:,}".format(player1API['karma']), self.worse,
                              font=font)
                    draw.text((1300, 1100), "Karma: {:,}".format(player2API['karma']), self.better,
                              font=font)
                if player1API['achievement_points'] > player2API['achievement_points']:
                    draw.text((0, 1300), "Achievement Points: {:,}".format(player1API['achievement_points']),
                              self.better,
                              font=font)
                    draw.text((1300, 1300), "Achievement Points: {:,}".format(player2API['achievement_points']),
                              self.worse,
                              font=font)
                elif player1API['achievement_points'] == player2API['achievement_points']:
                    draw.text((0, 1300), "Achievement Points: {:,}".format(player1API['achievement_points']),
                              self.same,
                              font=font)
                    draw.text((1300, 1300), "Achievement Points: {:,}".format(player2API['achievement_points']),
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1300), "Achievement Points: {:,}".format(player1API['achievement_points']),
                              self.worse,
                              font=font)
                    draw.text((1300, 1300), "Achievement Points: {:,}".format(player2API['achievement_points']),
                              self.better,
                              font=font)
                draw.text((0, 1500), f"Last Game: {player1API['last_game']}", self.neutral,
                          font=font)
                draw.text((1300, 1500), f"Last Game: {player2API['last_game']}", self.neutral,
                          font=font)

                draw.text((0, 1700), f"Online Status: {player1OnlineStatus}", self.neutral,
                          font=font)
                draw.text((1300, 1700), f"Online Status: {player2OnlineStatus}", self.neutral,
                          font=font)
                with io.BytesIO() as image_binary:
                    img.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))

            elif mode == "bedwars":
                img = Image.open("infoimgimg.png")
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("Minecraftia.ttf",
                                          65)
                fontbig = ImageFont.truetype("Minecraftia.ttf",
                                             250)
                draw.text((0, -100), "Bedwars:", self.neutral, font=fontbig)

                draw.text((0, 400), f"Username:\n{player1}", self.neutral,
                          font=font)
                draw.text((1300, 400), f"Username:\n{player2}", self.neutral,
                          font=font)
                if player1API['stats']['BedWars']['level'] > player2API['stats']['BedWars']['level']:
                    draw.text((0, 700), f"Star: {player1API['stats']['BedWars']['level']}", self.better,
                              font=font)
                    draw.text((1300, 700), f"Star: {player2API['stats']['BedWars']['level']}", self.worse,
                              font=font)
                elif player1API['stats']['BedWars']['level'] == player2API['stats']['BedWars']['level']:
                    draw.text((0, 700), f"Star: {player1API['stats']['BedWars']['level']}", self.same,
                              font=font)
                    draw.text((1300, 700), f"Star: {player2API['stats']['BedWars']['level']}", self.same,
                              font=font)
                else:
                    draw.text((0, 700), f"Star: {player1API['stats']['BedWars']['level']}", self.worse,
                              font=font)
                    draw.text((1300, 700), f"Star: {player2API['stats']['BedWars']['level']}", self.better,
                              font=font)

                if player1API['stats']['BedWars']['wins'] > player2API['stats']['BedWars']['wins']:
                    draw.text((0, 900), "Wins: {:,}".format(player1API['stats']['BedWars']['wins']), self.better,
                              font=font)
                    draw.text((1300, 900), "Wins: {:,}".format(player2API['stats']['BedWars']['wins']), self.worse,
                              font=font)
                elif player1API['stats']['BedWars']['wins'] == player2API['stats']['BedWars']['wins']:
                    draw.text((0, 900), "Wins: {:,}".format(player1API['stats']['BedWars']['wins']), self.same,
                              font=font)
                    draw.text((1300, 900), "Wins: {:,}".format(player2API['stats']['BedWars']['wins']), self.same,
                              font=font)
                else:
                    draw.text((0, 900), "Wins: {:,}".format(player1API['stats']['BedWars']['wins']), self.worse,
                              font=font)
                    draw.text((1300, 900), "Wins: {:,}".format(player2API['stats']['BedWars']['wins']), self.better,
                              font=font)

                if player1API['stats']['BedWars']['winstreak'] > player2API['stats']['BedWars']['winstreak']:
                    draw.text((0, 1100), f"Winstreak: {player1API['stats']['BedWars']['winstreak']}", self.better,
                              font=font)
                    draw.text((1300, 1100), f"Winstreak: {player2API['stats']['BedWars']['winstreak']}", self.worse,
                              font=font)
                elif player1API['stats']['BedWars']['winstreak'] == player2API['stats']['BedWars']['winstreak']:
                    draw.text((0, 1100), f"Winstreak: {player1API['stats']['BedWars']['winstreak']}", self.same,
                              font=font)
                    draw.text((1300, 1100), f"Winstreak: {player2API['stats']['BedWars']['winstreak']}",
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1100), f"Winstreak: {player1API['stats']['BedWars']['winstreak']}", self.worse,
                              font=font)
                    draw.text((1300, 1100), f"Winstreak: {player2API['stats']['BedWars']['winstreak']}",
                              self.better,
                              font=font)
                if player1API['stats']['BedWars']['final_k_d'] > player2API['stats']['BedWars']['final_k_d']:
                    draw.text((0, 1300), f"FKDR: {player1API['stats']['BedWars']['final_k_d']}", self.better,
                              font=font)
                    draw.text((1300, 1300), f"FKDR: {player2API['stats']['BedWars']['final_k_d']}", self.worse,
                              font=font)
                elif player1API['stats']['BedWars']['final_k_d'] == player2API['stats']['BedWars']['final_k_d']:
                    draw.text((0, 1300), f"FKDR: {player1API['stats']['BedWars']['final_k_d']}", self.same,
                              font=font)
                    draw.text((1300, 1300), f"FKDR: {player2API['stats']['BedWars']['final_k_d']}", self.same,
                              font=font)
                else:
                    draw.text((0, 1300), f"FKDR: {player1API['stats']['BedWars']['final_k_d']}", self.worse,
                              font=font)
                    draw.text((1300, 1300), f"FKDR: {player2API['stats']['BedWars']['final_k_d']}", self.better,
                              font=font)

                if player1API['stats']['BedWars']['final_kills'] > player2API['stats']['BedWars']['final_kills']:
                    draw.text((0, 1500), "Final Kills: {:,}".format(player1API['stats']['BedWars']['final_kills']),
                              self.better,
                              font=font)
                    draw.text((1300, 1500), "Final Kills: {:,}".format(player2API['stats']['BedWars']['final_kills']),
                              self.worse,
                              font=font)
                elif player1API['stats']['BedWars']['final_kills'] == player2API['stats']['BedWars']['final_kills']:
                    draw.text((0, 1500), "Final Kills: {:,}".format(player1API['stats']['BedWars']['final_kills']),
                              self.same,
                              font=font)
                    draw.text((1300, 1500), "Final Kills: {:,}".format(player2API['stats']['BedWars']['final_kills']),
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1500), "Final Kills: {:,}".format(player1API['stats']['BedWars']['final_kills']),
                              self.worse,
                              font=font)
                    draw.text((1300, 1500), "Final Kills: {:,}".format(player2API['stats']['BedWars']['final_kills']),
                              self.better,
                              font=font)
                if player1API['stats']['BedWars']['final_deaths'] > player2API['stats']['BedWars']['final_deaths']:
                    draw.text((0, 1700), "Final Deaths: {:,}".format(player1API['stats']['BedWars']['final_deaths']),
                              self.better,
                              font=font)
                    draw.text((1300, 1700), "Final Deaths: {:,}".format(player2API['stats']['BedWars']['final_deaths']),
                              self.worse,
                              font=font)
                elif player1API['stats']['BedWars']['final_deaths'] == player2API['stats']['BedWars']['final_deaths']:
                    draw.text((0, 1700), "Final Deaths: {:,}".format(player1API['stats']['BedWars']['final_deaths']),
                              self.same,
                              font=font)
                    draw.text((1300, 1700), "Final Deaths: {:,}".format(player2API['stats']['BedWars']['final_deaths']),
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1700), "Final Deaths: {:,}".format(player1API['stats']['BedWars']['final_deaths']),
                              self.worse,
                              font=font)
                    draw.text((1300, 1700), "Final Deaths: {:,}".format(player2API['stats']['BedWars']['final_deaths']),
                              self.better,
                              font=font)
                if player1API['stats']['BedWars']['beds_broken'] > player2API['stats']['BedWars']['beds_broken']:
                    draw.text((0, 1900), "Beds Broken: {:,}".format(player1API['stats']['BedWars']['beds_broken']),
                              self.better,
                              font=font)
                    draw.text((1300, 1900), "Beds Broken: {:,}".format(player2API['stats']['BedWars']['beds_broken']),
                              self.worse,
                              font=font)
                elif player1API['stats']['BedWars']['beds_broken'] == player2API['stats']['BedWars']['beds_broken']:
                    draw.text((0, 1900), "Beds Broken: {:,}".format(player1API['stats']['BedWars']['beds_broken']),
                              self.same,
                              font=font)
                    draw.text((1300, 1900), "Beds Broken: {:,}".format(player2API['stats']['BedWars']['beds_broken']),
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1900), "Beds Broken: {:,}".format(player1API['stats']['BedWars']['beds_broken']),
                              self.worse,
                              font=font)
                    draw.text((1300, 1900), "Beds Broken: {:,}".format(player2API['stats']['BedWars']['beds_broken']),
                              self.better,
                              font=font)
                with io.BytesIO() as image_binary:
                    img.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))

            elif mode == "bedwars_solo":
                fkdr1 = player1API['stats']['BedWars']['gamemodes']['solo']['final_kills'] / \
                        player1API['stats']['BedWars']['gamemodes']['solo']['final_deaths']
                fkdr2 = player2API['stats']['BedWars']['gamemodes']['solo']['final_kills'] / \
                        player2API['stats']['BedWars']['gamemodes']['solo']['final_deaths']
                img = Image.open("infoimgimg.png")
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("Minecraftia.ttf",
                                          65)
                fontbig = ImageFont.truetype("Minecraftia.ttf",
                                             250)
                draw.text((0, -100), "Bedwars Solo:", self.neutral, font=fontbig)

                draw.text((0, 400), f"Username:\n{player1}", self.neutral,
                          font=font)
                draw.text((1300, 400), f"Username:\n{player2}", self.neutral,
                          font=font)
                if player1API['stats']['BedWars']['gamemodes']['solo']['wins'] > \
                        player2API['stats']['BedWars']['gamemodes']['solo']['wins']:
                    draw.text((0, 700),
                              "Wins: {:,}".format(player1API['stats']['BedWars']['gamemodes']['solo']['wins']),
                              self.better,
                              font=font)
                    draw.text((1300, 700),
                              "Wins: {:,}".format(player2API['stats']['BedWars']['gamemodes']['solo']['wins']),
                              self.worse,
                              font=font)
                elif player1API['stats']['BedWars']['gamemodes']['solo']['wins'] == \
                        player2API['stats']['BedWars']['gamemodes']['solo']['wins']:
                    draw.text((0, 700),
                              "Wins: {:,}".format(player1API['stats']['BedWars']['gamemodes']['solo']['wins']),
                              self.same,
                              font=font)
                    draw.text((1300, 700),
                              "Wins: {:,}".format(player2API['stats']['BedWars']['gamemodes']['solo']['wins']),
                              self.same,
                              font=font)
                else:
                    draw.text((0, 700),
                              "Wins: {:,}".format(player1API['stats']['BedWars']['gamemodes']['solo']['wins']),
                              self.worse,
                              font=font)
                    draw.text((1300, 700),
                              "Wins: {:,}".format(player2API['stats']['BedWars']['gamemodes']['solo']['wins']),
                              self.better,
                              font=font)
                if player1API['stats']['BedWars']['gamemodes']['solo']['losses'] > \
                        player2API['stats']['BedWars']['gamemodes']['solo']['losses']:
                    draw.text((0, 900),
                              "Losses: {:,}".format(player1API['stats']['BedWars']['gamemodes']['solo']['losses']),
                              self.better,
                              font=font)
                    draw.text((1300, 900),
                              "Losses: {:,}".format(player2API['stats']['BedWars']['gamemodes']['solo']['losses']),
                              self.worse,
                              font=font)
                elif player1API['stats']['BedWars']['gamemodes']['solo']['losses'] == \
                        player2API['stats']['BedWars']['gamemodes']['solo']['losses']:
                    draw.text((0, 900),
                              "Losses: {:,}".format(player1API['stats']['BedWars']['gamemodes']['solo']['losses']),
                              self.same,
                              font=font)
                    draw.text((1300, 900),
                              "Losses: {:,}".format(player2API['stats']['BedWars']['gamemodes']['solo']['losses']),
                              self.same,
                              font=font)
                else:
                    draw.text((0, 900),
                              "Losses: {:,}".format(player1API['stats']['BedWars']['gamemodes']['solo']['losses']),
                              self.worse,
                              font=font)
                    draw.text((1300, 900),
                              "Losses: {:,}".format(player2API['stats']['BedWars']['gamemodes']['solo']['losses']),
                              self.better,
                              font=font)
                if player1API['stats']['BedWars']['gamemodes']['solo']['winstreak'] > \
                        player2API['stats']['BedWars']['gamemodes']['solo']['winstreak']:
                    draw.text((0, 1100),
                              f"Winstreak: {player1API['stats']['BedWars']['gamemodes']['solo']['winstreak']}",
                              self.better,
                              font=font)
                    draw.text((1300, 1100),
                              f"Winstreak: {player2API['stats']['BedWars']['gamemodes']['solo']['winstreak']}",
                              self.worse,
                              font=font)
                elif player1API['stats']['BedWars']['gamemodes']['solo']['winstreak'] == \
                        player2API['stats']['BedWars']['gamemodes']['solo']['winstreak']:
                    draw.text((0, 1100),
                              f"Winstreak: {player1API['stats']['BedWars']['gamemodes']['solo']['winstreak']}",
                              self.same,
                              font=font)
                    draw.text((1300, 1100),
                              f"Winstreak: {player2API['stats']['BedWars']['gamemodes']['solo']['winstreak']}",
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1100),
                              f"Winstreak: {player1API['stats']['BedWars']['gamemodes']['solo']['winstreak']}",
                              self.worse,
                              font=font)
                    draw.text((1300, 1100),
                              f"Winstreak: {player2API['stats']['BedWars']['gamemodes']['solo']['winstreak']}",
                              self.better,
                              font=font)
                if fkdr1 > fkdr2:
                    draw.text((0, 1300), f"FKDR: %.2f" % fkdr1, self.better,
                              font=font)
                    draw.text((1300, 1300), f"FKDR %.2f" % fkdr2, self.worse,
                              font=font)
                elif fkdr1 == fkdr2:
                    draw.text((0, 1300), f"FKDR: %.2f" % fkdr1, self.same,
                              font=font)
                    draw.text((1300, 1300), f"FKDR %.2f" % fkdr2, self.same,
                              font=font)
                else:
                    draw.text((0, 1300), f"FKDR: %.2f" % fkdr1, self.worse,
                              font=font)
                    draw.text((1300, 1300), f"FKDR %.2f" % fkdr2, self.better,
                              font=font)

                if player1API['stats']['BedWars']['gamemodes']['solo']['final_kills'] > \
                        player2API['stats']['BedWars']['gamemodes']['solo']['final_kills']:
                    draw.text((0, 1500),
                              "Final Kills: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['solo']['final_kills']),
                              self.better,
                              font=font)
                    draw.text((1300, 1500),
                              "Final Kills: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['solo']['final_kills']),
                              self.worse,
                              font=font)
                elif player1API['stats']['BedWars']['gamemodes']['solo']['final_kills'] == \
                        player2API['stats']['BedWars']['gamemodes']['solo']['final_kills']:
                    draw.text((0, 1500),
                              "Final Kills: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['solo']['final_kills']),
                              self.same,
                              font=font)
                    draw.text((1300, 1500),
                              "Final Kills: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['solo']['final_kills']),
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1500),
                              "Final Kills: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['solo']['final_kills']),
                              self.worse,
                              font=font)
                    draw.text((1300, 1500),
                              "Final Kills: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['solo']['final_kills']),
                              self.better,
                              font=font)
                if player1API['stats']['BedWars']['gamemodes']['solo']['final_deaths'] > \
                        player2API['stats']['BedWars']['gamemodes']['solo']['final_deaths']:
                    draw.text((0, 1700),
                              "Final Deaths: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['solo']['final_deaths']),
                              self.better,
                              font=font)
                    draw.text((1300, 1700),
                              "Final Deaths: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['solo']['final_deaths']),
                              self.worse,
                              font=font)
                elif player1API['stats']['BedWars']['gamemodes']['solo']['final_deaths'] == \
                        player2API['stats']['BedWars']['gamemodes']['solo']['final_deaths']:
                    draw.text((0, 1700),
                              "Final Deaths: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['solo']['final_deaths']),
                              self.same,
                              font=font)
                    draw.text((1300, 1700),
                              "Final Deaths: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['solo']['final_deaths']),
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1700),
                              "Final Deaths: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['solo']['final_deaths']),
                              self.worse,
                              font=font)
                    draw.text((1300, 1700),
                              "Final Deaths: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['solo']['final_deaths']),
                              self.better,
                              font=font)
                if player1API['stats']['BedWars']['gamemodes']['solo']['beds_broken'] > \
                        player2API['stats']['BedWars']['gamemodes']['solo']['beds_broken']:
                    draw.text((0, 1900),
                              "Beds Broken: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['solo']['beds_broken']),
                              self.better,
                              font=font)
                    draw.text((1300, 1900),
                              "Beds Broken: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['solo']['beds_broken']),
                              self.worse,
                              font=font)
                elif player1API['stats']['BedWars']['gamemodes']['solo']['beds_broken'] == \
                        player2API['stats']['BedWars']['gamemodes']['solo']['beds_broken']:
                    draw.text((0, 1900),
                              "Beds Broken: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['solo']['beds_broken']),
                              self.same,
                              font=font)
                    draw.text((1300, 1900),
                              "Beds Broken: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['solo']['beds_broken']),
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1900),
                              "Beds Broken: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['solo']['beds_broken']),
                              self.worse,
                              font=font)
                    draw.text((1300, 1900),
                              "Beds Broken: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['solo']['beds_broken']),
                              self.better,
                              font=font)
                with io.BytesIO() as image_binary:
                    img.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))

            elif mode == "bedwars_doubles":
                fkdr1 = player1API['stats']['BedWars']['gamemodes']['doubles']['final_kills'] / \
                        player1API['stats']['BedWars']['gamemodes']['doubles']['final_deaths']
                fkdr2 = player2API['stats']['BedWars']['gamemodes']['doubles']['final_kills'] / \
                        player2API['stats']['BedWars']['gamemodes']['doubles']['final_deaths']
                img = Image.open("infoimgimg.png")
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("Minecraftia.ttf",
                                          65)
                fontbig = ImageFont.truetype("Minecraftia.ttf",
                                             210)
                draw.text((0, -80), "Bedwars doubles:", self.neutral, font=fontbig)

                draw.text((0, 400), f"Username:\n{player1}", self.neutral,
                          font=font)
                draw.text((1300, 400), f"Username:\n{player2}", self.neutral,
                          font=font)
                if player1API['stats']['BedWars']['gamemodes']['doubles']['wins'] > \
                        player2API['stats']['BedWars']['gamemodes']['doubles']['wins']:
                    draw.text((0, 700),
                              "Wins: {:,}".format(player1API['stats']['BedWars']['gamemodes']['doubles']['wins']),
                              self.better,
                              font=font)
                    draw.text((1300, 700),
                              "Wins: {:,}".format(player2API['stats']['BedWars']['gamemodes']['doubles']['wins']),
                              self.worse,
                              font=font)
                elif player1API['stats']['BedWars']['gamemodes']['doubles']['wins'] == \
                        player2API['stats']['BedWars']['gamemodes']['doubles']['wins']:
                    draw.text((0, 700),
                              "Wins: {:,}".format(player1API['stats']['BedWars']['gamemodes']['doubles']['wins']),
                              self.same,
                              font=font)
                    draw.text((1300, 700),
                              "Wins: {:,}".format(player2API['stats']['BedWars']['gamemodes']['doubles']['wins']),
                              self.same,
                              font=font)
                else:
                    draw.text((0, 700),
                              "Wins: {:,}".format(player1API['stats']['BedWars']['gamemodes']['doubles']['wins']),
                              self.worse,
                              font=font)
                    draw.text((1300, 700),
                              "Wins: {:,}".format(player2API['stats']['BedWars']['gamemodes']['doubles']['wins']),
                              self.better,
                              font=font)
                if player1API['stats']['BedWars']['gamemodes']['doubles']['losses'] > \
                        player2API['stats']['BedWars']['gamemodes']['doubles']['losses']:
                    draw.text((0, 900),
                              "Losses: {:,}".format(player1API['stats']['BedWars']['gamemodes']['doubles']['losses']),
                              self.better,
                              font=font)
                    draw.text((1300, 900),
                              "Losses: {:,}".format(player2API['stats']['BedWars']['gamemodes']['doubles']['losses']),
                              self.worse,
                              font=font)
                elif player1API['stats']['BedWars']['gamemodes']['doubles']['losses'] == \
                        player2API['stats']['BedWars']['gamemodes']['doubles']['losses']:
                    draw.text((0, 900),
                              "Losses: {:,}".format(player1API['stats']['BedWars']['gamemodes']['doubles']['losses']),
                              self.same,
                              font=font)
                    draw.text((1300, 900),
                              "Losses: {:,}".format(player2API['stats']['BedWars']['gamemodes']['doubles']['losses']),
                              self.same,
                              font=font)
                else:
                    draw.text((0, 900),
                              "Losses: {:,}".format(player1API['stats']['BedWars']['gamemodes']['doubles']['losses']),
                              self.worse,
                              font=font)
                    draw.text((1300, 900),
                              "Losses: {:,}".format(player2API['stats']['BedWars']['gamemodes']['doubles']['losses']),
                              self.better,
                              font=font)
                if player1API['stats']['BedWars']['gamemodes']['doubles']['winstreak'] > \
                        player2API['stats']['BedWars']['gamemodes']['doubles']['winstreak']:
                    draw.text((0, 1100),
                              f"Winstreak: {player1API['stats']['BedWars']['gamemodes']['doubles']['winstreak']}",
                              self.better,
                              font=font)
                    draw.text((1300, 1100),
                              f"Winstreak: {player2API['stats']['BedWars']['gamemodes']['doubles']['winstreak']}",
                              self.worse,
                              font=font)
                elif player1API['stats']['BedWars']['gamemodes']['doubles']['winstreak'] == \
                        player2API['stats']['BedWars']['gamemodes']['doubles']['winstreak']:
                    draw.text((0, 1100),
                              f"Winstreak: {player1API['stats']['BedWars']['gamemodes']['doubles']['winstreak']}",
                              self.same,
                              font=font)
                    draw.text((1300, 1100),
                              f"Winstreak: {player2API['stats']['BedWars']['gamemodes']['doubles']['winstreak']}",
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1100),
                              f"Winstreak: {player1API['stats']['BedWars']['gamemodes']['doubles']['winstreak']}",
                              self.worse,
                              font=font)
                    draw.text((1300, 1100),
                              f"Winstreak: {player2API['stats']['BedWars']['gamemodes']['doubles']['winstreak']}",
                              self.better,
                              font=font)
                if fkdr1 > fkdr2:
                    draw.text((0, 1300), f"FKDR: %.2f" % fkdr1, self.better,
                              font=font)
                    draw.text((1300, 1300), f"FKDR %.2f" % fkdr2, self.worse,
                              font=font)
                elif fkdr1 == fkdr2:
                    draw.text((0, 1300), f"FKDR: %.2f" % fkdr1, self.same,
                              font=font)
                    draw.text((1300, 1300), f"FKDR %.2f" % fkdr2, self.same,
                              font=font)
                else:
                    draw.text((0, 1300), f"FKDR: %.2f" % fkdr1, self.worse,
                              font=font)
                    draw.text((1300, 1300), f"FKDR %.2f" % fkdr2, self.better,
                              font=font)

                if player1API['stats']['BedWars']['gamemodes']['doubles']['final_kills'] > \
                        player2API['stats']['BedWars']['gamemodes']['doubles']['final_kills']:
                    draw.text((0, 1500),
                              "Final Kills: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['doubles']['final_kills']),
                              self.better,
                              font=font)
                    draw.text((1300, 1500),
                              "Final Kills: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['doubles']['final_kills']),
                              self.worse,
                              font=font)
                elif player1API['stats']['BedWars']['gamemodes']['doubles']['final_kills'] == \
                        player2API['stats']['BedWars']['gamemodes']['doubles']['final_kills']:
                    draw.text((0, 1500),
                              "Final Kills: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['doubles']['final_kills']),
                              self.same,
                              font=font)
                    draw.text((1300, 1500),
                              "Final Kills: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['doubles']['final_kills']),
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1500),
                              "Final Kills: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['doubles']['final_kills']),
                              self.worse,
                              font=font)
                    draw.text((1300, 1500),
                              "Final Kills: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['doubles']['final_kills']),
                              self.better,
                              font=font)
                if player1API['stats']['BedWars']['gamemodes']['doubles']['final_deaths'] > \
                        player2API['stats']['BedWars']['gamemodes']['doubles']['final_deaths']:
                    draw.text((0, 1700),
                              "Final Deaths: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['doubles']['final_deaths']),
                              self.better,
                              font=font)
                    draw.text((1300, 1700),
                              "Final Deaths: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['doubles']['final_deaths']),
                              self.worse,
                              font=font)
                elif player1API['stats']['BedWars']['gamemodes']['doubles']['final_deaths'] == \
                        player2API['stats']['BedWars']['gamemodes']['doubles']['final_deaths']:
                    draw.text((0, 1700),
                              "Final Deaths: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['doubles']['final_deaths']),
                              self.same,
                              font=font)
                    draw.text((1300, 1700),
                              "Final Deaths: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['doubles']['final_deaths']),
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1700),
                              "Final Deaths: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['doubles']['final_deaths']),
                              self.worse,
                              font=font)
                    draw.text((1300, 1700),
                              "Final Deaths: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['doubles']['final_deaths']),
                              self.better,
                              font=font)
                if player1API['stats']['BedWars']['gamemodes']['doubles']['beds_broken'] > \
                        player2API['stats']['BedWars']['gamemodes']['doubles']['beds_broken']:
                    draw.text((0, 1900),
                              "Beds Broken: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['doubles']['beds_broken']),
                              self.better,
                              font=font)
                    draw.text((1300, 1900),
                              "Beds Broken: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['doubles']['beds_broken']),
                              self.worse,
                              font=font)
                elif player1API['stats']['BedWars']['gamemodes']['doubles']['beds_broken'] == \
                        player2API['stats']['BedWars']['gamemodes']['doubles']['beds_broken']:
                    draw.text((0, 1900),
                              "Beds Broken: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['doubles']['beds_broken']),
                              self.same,
                              font=font)
                    draw.text((1300, 1900),
                              "Beds Broken: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['doubles']['beds_broken']),
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1900),
                              "Beds Broken: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['doubles']['beds_broken']),
                              self.worse,
                              font=font)
                    draw.text((1300, 1900),
                              "Beds Broken: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['doubles']['beds_broken']),
                              self.better,
                              font=font)
                with io.BytesIO() as image_binary:
                    img.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))

            elif mode in ("bedwars_threes", "bedwars_three", "bedwars_3"):
                fkdr1 = player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_kills'] / \
                        player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_deaths']
                fkdr2 = player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_kills'] / \
                        player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_deaths']
                img = Image.open("infoimgimg.png")
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("Minecraftia.ttf",
                                          65)
                fontbig = ImageFont.truetype("Minecraftia.ttf",
                                             210)
                draw.text((0, -80), "Bedwars 3v3v3v3:", self.neutral, font=fontbig)

                draw.text((0, 400), f"Username:\n{player1}", self.neutral,
                          font=font)
                draw.text((1300, 400), f"Username:\n{player2}", self.neutral,
                          font=font)
                if player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['wins'] > \
                        player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['wins']:
                    draw.text((0, 700),
                              "Wins: {:,}".format(player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['wins']),
                              self.better,
                              font=font)
                    draw.text((1300, 700),
                              "Wins: {:,}".format(player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['wins']),
                              self.worse,
                              font=font)
                elif player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['wins'] == \
                        player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['wins']:
                    draw.text((0, 700),
                              "Wins: {:,}".format(player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['wins']),
                              self.same,
                              font=font)
                    draw.text((1300, 700),
                              "Wins: {:,}".format(player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['wins']),
                              self.same,
                              font=font)
                else:
                    draw.text((0, 700),
                              "Wins: {:,}".format(player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['wins']),
                              self.worse,
                              font=font)
                    draw.text((1300, 700),
                              "Wins: {:,}".format(player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['wins']),
                              self.better,
                              font=font)
                if player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['losses'] > \
                        player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['losses']:
                    draw.text((0, 900),
                              "Losses: {:,}".format(player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['losses']),
                              self.better,
                              font=font)
                    draw.text((1300, 900),
                              "Losses: {:,}".format(player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['losses']),
                              self.worse,
                              font=font)
                elif player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['losses'] == \
                        player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['losses']:
                    draw.text((0, 900),
                              "Losses: {:,}".format(player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['losses']),
                              self.same,
                              font=font)
                    draw.text((1300, 900),
                              "Losses: {:,}".format(player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['losses']),
                              self.same,
                              font=font)
                else:
                    draw.text((0, 900),
                              "Losses: {:,}".format(player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['losses']),
                              self.worse,
                              font=font)
                    draw.text((1300, 900),
                              "Losses: {:,}".format(player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['losses']),
                              self.better,
                              font=font)
                if player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['winstreak'] > \
                        player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['winstreak']:
                    draw.text((0, 1100),
                              f"Winstreak: {player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['winstreak']}",
                              self.better,
                              font=font)
                    draw.text((1300, 1100),
                              f"Winstreak: {player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['winstreak']}",
                              self.worse,
                              font=font)
                elif player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['winstreak'] == \
                        player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['winstreak']:
                    draw.text((0, 1100),
                              f"Winstreak: {player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['winstreak']}",
                              self.same,
                              font=font)
                    draw.text((1300, 1100),
                              f"Winstreak: {player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['winstreak']}",
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1100),
                              f"Winstreak: {player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['winstreak']}",
                              self.worse,
                              font=font)
                    draw.text((1300, 1100),
                              f"Winstreak: {player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['winstreak']}",
                              self.better,
                              font=font)
                if fkdr1 > fkdr2:
                    draw.text((0, 1300), f"FKDR: %.2f" % fkdr1, self.better,
                              font=font)
                    draw.text((1300, 1300), f"FKDR %.2f" % fkdr2, self.worse,
                              font=font)
                elif fkdr1 == fkdr2:
                    draw.text((0, 1300), f"FKDR: %.2f" % fkdr1, self.same,
                              font=font)
                    draw.text((1300, 1300), f"FKDR %.2f" % fkdr2, self.same,
                              font=font)
                else:
                    draw.text((0, 1300), f"FKDR: %.2f" % fkdr1, self.worse,
                              font=font)
                    draw.text((1300, 1300), f"FKDR %.2f" % fkdr2, self.better,
                              font=font)

                if player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_kills'] > \
                        player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_kills']:
                    draw.text((0, 1500),
                              "Final Kills: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_kills']),
                              self.better,
                              font=font)
                    draw.text((1300, 1500),
                              "Final Kills: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_kills']),
                              self.worse,
                              font=font)
                elif player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_kills'] == \
                        player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_kills']:
                    draw.text((0, 1500),
                              "Final Kills: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_kills']),
                              self.same,
                              font=font)
                    draw.text((1300, 1500),
                              "Final Kills: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_kills']),
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1500),
                              "Final Kills: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_kills']),
                              self.worse,
                              font=font)
                    draw.text((1300, 1500),
                              "Final Kills: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_kills']),
                              self.better,
                              font=font)
                if player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_deaths'] > \
                        player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_deaths']:
                    draw.text((0, 1700),
                              "Final Deaths: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_deaths']),
                              self.better,
                              font=font)
                    draw.text((1300, 1700),
                              "Final Deaths: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_deaths']),
                              self.worse,
                              font=font)
                elif player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_deaths'] == \
                        player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_deaths']:
                    draw.text((0, 1700),
                              "Final Deaths: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_deaths']),
                              self.same,
                              font=font)
                    draw.text((1300, 1700),
                              "Final Deaths: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_deaths']),
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1700),
                              "Final Deaths: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_deaths']),
                              self.worse,
                              font=font)
                    draw.text((1300, 1700),
                              "Final Deaths: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_deaths']),
                              self.better,
                              font=font)
                if player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['beds_broken'] > \
                        player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['beds_broken']:
                    draw.text((0, 1900),
                              "Beds Broken: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['beds_broken']),
                              self.better,
                              font=font)
                    draw.text((1300, 1900),
                              "Beds Broken: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['beds_broken']),
                              self.worse,
                              font=font)
                elif player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['beds_broken'] == \
                        player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['beds_broken']:
                    draw.text((0, 1900),
                              "Beds Broken: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['beds_broken']),
                              self.same,
                              font=font)
                    draw.text((1300, 1900),
                              "Beds Broken: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['beds_broken']),
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1900),
                              "Beds Broken: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['beds_broken']),
                              self.worse,
                              font=font)
                    draw.text((1300, 1900),
                              "Beds Broken: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['beds_broken']),
                              self.better,
                              font=font)
                with io.BytesIO() as image_binary:
                    img.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))

            elif mode in ("bedwars_fours", "bedwars_four", "bedwars_4"):
                fkdr1 = player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_kills'] / \
                        player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_deaths']
                fkdr2 = player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_kills'] / \
                        player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_deaths']
                img = Image.open("infoimgimg.png")
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("Minecraftia.ttf",
                                          65)
                fontbig = ImageFont.truetype("Minecraftia.ttf",
                                             210)
                draw.text((0, -80), "Bedwars 4v4v4v4:", self.neutral, font=fontbig)

                draw.text((0, 400), f"Username:\n{player1}", self.neutral,
                          font=font)
                draw.text((1300, 400), f"Username:\n{player2}", self.neutral,
                          font=font)
                if player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['wins'] > \
                        player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['wins']:
                    draw.text((0, 700),
                              "Wins: {:,}".format(player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['wins']),
                              self.better,
                              font=font)
                    draw.text((1300, 700),
                              "Wins: {:,}".format(player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['wins']),
                              self.worse,
                              font=font)
                elif player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['wins'] == \
                        player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['wins']:
                    draw.text((0, 700),
                              "Wins: {:,}".format(player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['wins']),
                              self.same,
                              font=font)
                    draw.text((1300, 700),
                              "Wins: {:,}".format(player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['wins']),
                              self.same,
                              font=font)
                else:
                    draw.text((0, 700),
                              "Wins: {:,}".format(player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['wins']),
                              self.worse,
                              font=font)
                    draw.text((1300, 700),
                              "Wins: {:,}".format(player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['wins']),
                              self.better,
                              font=font)
                if player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['losses'] > \
                        player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['losses']:
                    draw.text((0, 900),
                              "Losses: {:,}".format(player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['losses']),
                              self.better,
                              font=font)
                    draw.text((1300, 900),
                              "Losses: {:,}".format(player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['losses']),
                              self.worse,
                              font=font)
                elif player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['losses'] == \
                        player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['losses']:
                    draw.text((0, 900),
                              "Losses: {:,}".format(player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['losses']),
                              self.same,
                              font=font)
                    draw.text((1300, 900),
                              "Losses: {:,}".format(player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['losses']),
                              self.same,
                              font=font)
                else:
                    draw.text((0, 900),
                              "Losses: {:,}".format(player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['losses']),
                              self.worse,
                              font=font)
                    draw.text((1300, 900),
                              "Losses: {:,}".format(player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['losses']),
                              self.better,
                              font=font)
                if player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['winstreak'] > \
                        player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['winstreak']:
                    draw.text((0, 1100),
                              f"Winstreak: {player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['winstreak']}",
                              self.better,
                              font=font)
                    draw.text((1300, 1100),
                              f"Winstreak: {player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['winstreak']}",
                              self.worse,
                              font=font)
                elif player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['winstreak'] == \
                        player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['winstreak']:
                    draw.text((0, 1100),
                              f"Winstreak: {player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['winstreak']}",
                              self.same,
                              font=font)
                    draw.text((1300, 1100),
                              f"Winstreak: {player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['winstreak']}",
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1100),
                              f"Winstreak: {player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['winstreak']}",
                              self.worse,
                              font=font)
                    draw.text((1300, 1100),
                              f"Winstreak: {player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['winstreak']}",
                              self.better,
                              font=font)
                if fkdr1 > fkdr2:
                    draw.text((0, 1300), f"FKDR: %.2f" % fkdr1, self.better,
                              font=font)
                    draw.text((1300, 1300), f"FKDR %.2f" % fkdr2, self.worse,
                              font=font)
                elif fkdr1 == fkdr2:
                    draw.text((0, 1300), f"FKDR: %.2f" % fkdr1, self.same,
                              font=font)
                    draw.text((1300, 1300), f"FKDR %.2f" % fkdr2, self.same,
                              font=font)
                else:
                    draw.text((0, 1300), f"FKDR: %.2f" % fkdr1, self.worse,
                              font=font)
                    draw.text((1300, 1300), f"FKDR %.2f" % fkdr2, self.better,
                              font=font)

                if player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_kills'] > \
                        player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_kills']:
                    draw.text((0, 1500),
                              "Final Kills: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_kills']),
                              self.better,
                              font=font)
                    draw.text((1300, 1500),
                              "Final Kills: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_kills']),
                              self.worse,
                              font=font)
                elif player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_kills'] == \
                        player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_kills']:
                    draw.text((0, 1500),
                              "Final Kills: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_kills']),
                              self.same,
                              font=font)
                    draw.text((1300, 1500),
                              "Final Kills: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_kills']),
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1500),
                              "Final Kills: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_kills']),
                              self.worse,
                              font=font)
                    draw.text((1300, 1500),
                              "Final Kills: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_kills']),
                              self.better,
                              font=font)
                if player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_deaths'] > \
                        player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_deaths']:
                    draw.text((0, 1700),
                              "Final Deaths: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_deaths']),
                              self.better,
                              font=font)
                    draw.text((1300, 1700),
                              "Final Deaths: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_deaths']),
                              self.worse,
                              font=font)
                elif player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_deaths'] == \
                        player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_deaths']:
                    draw.text((0, 1700),
                              "Final Deaths: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_deaths']),
                              self.same,
                              font=font)
                    draw.text((1300, 1700),
                              "Final Deaths: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_deaths']),
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1700),
                              "Final Deaths: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_deaths']),
                              self.worse,
                              font=font)
                    draw.text((1300, 1700),
                              "Final Deaths: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_deaths']),
                              self.better,
                              font=font)
                if player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['beds_broken'] > \
                        player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['beds_broken']:
                    draw.text((0, 1900),
                              "Beds Broken: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['beds_broken']),
                              self.better,
                              font=font)
                    draw.text((1300, 1900),
                              "Beds Broken: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['beds_broken']),
                              self.worse,
                              font=font)
                elif player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['beds_broken'] == \
                        player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['beds_broken']:
                    draw.text((0, 1900),
                              "Beds Broken: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['beds_broken']),
                              self.same,
                              font=font)
                    draw.text((1300, 1900),
                              "Beds Broken: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['beds_broken']),
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1900),
                              "Beds Broken: {:,}".format(
                                  player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['beds_broken']),
                              self.worse,
                              font=font)
                    draw.text((1300, 1900),
                              "Beds Broken: {:,}".format(
                                  player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['beds_broken']),
                              self.better,
                              font=font)
                with io.BytesIO() as image_binary:
                    img.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))

            elif mode in ("duel", "duels"):
                img = Image.open("infoimgimg.png")
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("Minecraftia.ttf",
                                          65)
                fontbig = ImageFont.truetype("Minecraftia.ttf",
                                             250)
                draw.text((0, -100), "Duels:", self.neutral, font=fontbig)

                draw.text((0, 400), f"Username:\n{player1}", self.neutral,
                          font=font)
                draw.text((1300, 400), f"Username:\n{player2}", self.neutral,
                          font=font)
                if 'cosmetictitle' in player1API['stats']['Duels']['settings']['active_cosmetics']:
                    draw.text((0, 700),
                              f"Title: {player1API['stats']['Duels']['settings']['active_cosmetics']['cosmetictitle']}",
                              self.neutral,
                              font=font)
                else:
                    draw.text((0, 700), f"Title: None",
                              self.neutral,
                              font=font)

                if 'cosmetictitle' in player2API['stats']['Duels']['settings']['active_cosmetics']:
                    draw.text((1300, 700),
                              f"Title: {player2API['stats']['Duels']['settings']['active_cosmetics']['cosmetictitle']}",
                              self.neutral,
                              font=font)
                else:
                    draw.text((1300, 700), f"Title: None",
                              self.neutral,
                              font=font)
                if player1API['stats']['Duels']['general']['wins'] > player2API['stats']['Duels']['general']['wins']:
                    draw.text((0, 900), "Wins: {:,}".format(player1API['stats']['Duels']['general']['wins']),
                              self.better,
                              font=font)
                    draw.text((1300, 900), "Wins: {:,}".format(player2API['stats']['Duels']['general']['wins']),
                              self.worse,
                              font=font)
                elif player1API['stats']['Duels']['general']['wins'] == player1API['stats']['Duels']['general']['wins']:
                    draw.text((0, 900), "Wins: {:,}".format(player1API['stats']['Duels']['general']['wins']),
                              self.same,
                              font=font)
                    draw.text((1300, 900), "Wins: {:,}".format(player2API['stats']['Duels']['general']['wins']),
                              self.same,
                              font=font)
                else:
                    draw.text((0, 900), "Wins: {:,}".format(player1API['stats']['Duels']['general']['wins']),
                              self.worse,
                              font=font)
                    draw.text((1300, 900), "Wins: {:,}".format(player2API['stats']['Duels']['general']['wins']),
                              self.better,
                              font=font)
                if player1API['stats']['Duels']['general']['losses'] > player2API['stats']['Duels']['general'][
                    'losses']:
                    draw.text((0, 1100), "Losses: {:,}".format(player1API['stats']['Duels']['general']['losses']),
                              self.better,
                              font=font)
                    draw.text((1300, 1100), "Losses: {:,}".format(player2API['stats']['Duels']['general']['losses']),
                              self.worse,
                              font=font)
                elif player1API['stats']['Duels']['general']['losses'] == player2API['stats']['Duels']['general'][
                    'losses']:
                    draw.text((0, 1100), "Losses: {:,}".format(player1API['stats']['Duels']['general']['losses']),
                              self.same,
                              font=font)
                    draw.text((1300, 1100), "Losses: {:,}".format(player2API['stats']['Duels']['general']['losses']),
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1100), "Losses: {:,}".format(player1API['stats']['Duels']['general']['losses']),
                              self.worse,
                              font=font)
                    draw.text((1300, 1100), "Losses: {:,}".format(player2API['stats']['Duels']['general']['losses']),
                              self.better,
                              font=font)
                if player1API['stats']['Duels']['general']['kills'] > player2API['stats']['Duels']['general']['kills']:
                    draw.text((0, 1300), f"Kills: {player1API['stats']['Duels']['general']['kills']:,}",
                              self.better,
                              font=font)
                    draw.text((1300, 1300), f"Kills: {player2API['stats']['Duels']['general']['kills']:,}",
                              self.worse,
                              font=font)
                elif player1API['stats']['Duels']['general']['kills'] == player2API['stats']['Duels']['general'][
                    'kills']:
                    draw.text((0, 1300), f"Kills: {player1API['stats']['Duels']['general']['kills']:,}",
                              self.same,
                              font=font)
                    draw.text((1300, 1300), f"Kills: {player2API['stats']['Duels']['general']['kills']:,}",
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1300), f"Kills: {player1API['stats']['Duels']['general']['kills']:,}",
                              self.worse,
                              font=font)
                    draw.text((1300, 1300), f"Kills: {player2API['stats']['Duels']['general']['kills']:,}",
                              self.better,
                              font=font)

                if player1API['stats']['Duels']['general']['deaths'] > player2API['stats']['Duels']['general'][
                    'deaths']:
                    draw.text((0, 1500), f"Deaths: {player1API['stats']['Duels']['general']['deaths']:,}",
                              self.better,
                              font=font)
                    draw.text((1300, 1500), f"Deaths: {player2API['stats']['Duels']['general']['deaths']:,}",
                              self.worse,
                              font=font)
                elif player1API['stats']['Duels']['general']['deaths'] == player2API['stats']['Duels']['general'][
                    'deaths']:
                    draw.text((0, 1500), f"Deaths: {player1API['stats']['Duels']['general']['deaths']:,}",
                              self.same,
                              font=font)
                    draw.text((1300, 1500), f"Deaths: {player2API['stats']['Duels']['general']['deaths']:,}",
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1500), f"Deaths: {player1API['stats']['Duels']['general']['deaths']:,}",
                              self.worse,
                              font=font)
                    draw.text((1300, 1500), f"Deaths: {player2API['stats']['Duels']['general']['deaths']:,}",
                              self.better,
                              font=font)

                if player1API['stats']['Duels']['general']['kd_ratio'] > player2API['stats']['Duels']['general'][
                    'kd_ratio']:
                    draw.text((0, 1700), f"KDR: %.2f" % player1API['stats']['Duels']['general']['kd_ratio'],
                              self.better,
                              font=font)
                    draw.text((1300, 1700), f"KDR: %.2f" % player2API['stats']['Duels']['general']['kd_ratio'],
                              self.worse,
                              font=font)
                elif player1API['stats']['Duels']['general']['kd_ratio'] == player2API['stats']['Duels']['general'][
                    'kd_ratio']:
                    draw.text((0, 1700), f"KDR: %.2f" % player1API['stats']['Duels']['general']['kd_ratio'],
                              self.same,
                              font=font)
                    draw.text((1300, 1700), f"KDR: %.2f" % player2API['stats']['Duels']['general']['kd_ratio'],
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1700), f"KDR: %.2f" % player1API['stats']['Duels']['general']['kd_ratio'],
                              self.worse,
                              font=font)
                    draw.text((1300, 1700), f"KDR: %.2f" % player2API['stats']['Duels']['general']['kd_ratio'],
                              self.better,
                              font=font)

                with io.BytesIO() as image_binary:
                    img.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))

            elif mode in ("blitz"):
                img = Image.open("infoimgimg.png")
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("Minecraftia.ttf",
                                          65)
                fontbig = ImageFont.truetype("Minecraftia.ttf",
                                             250)
                draw.text((0, -100), "Blitz:", self.neutral, font=fontbig)

                draw.text((0, 400), f"Username:\n{player1}", self.neutral,
                          font=font)
                draw.text((1300, 400), f"Username:\n{player2}", self.neutral,
                          font=font)

                if player1API['stats']['Blitz']['wins'] > player2API['stats']['Blitz']['wins']:
                    draw.text((0, 700), f"Wins: {player1API['stats']['Blitz']['wins']:,}",
                              self.better,
                              font=font)
                    draw.text((1300, 700), f"Wins: {player2API['stats']['Blitz']['wins']:,}",
                              self.worse,
                              font=font)
                elif player1API['stats']['Blitz']['wins'] == player2API['stats']['Blitz']['wins']:
                    draw.text((0, 700), f"Wins: {player1API['stats']['Blitz']['wins']:,}",
                              self.same,
                              font=font)
                    draw.text((1300, 700), f"Wins: {player2API['stats']['Blitz']['wins']:,}",
                              self.same,
                              font=font)
                else:
                    draw.text((0, 700), f"Wins: {player1API['stats']['Blitz']['wins']:,}",
                              self.worse,
                              font=font)
                    draw.text((1300, 700), f"Wins: {player2API['stats']['Blitz']['wins']:,}",
                              self.better,
                              font=font)

                if player1API['stats']['Blitz']['kills'] > player2API['stats']['Blitz']['kills']:
                    draw.text((0, 900), f"Kills: {player1API['stats']['Blitz']['kills']:,}",
                              self.better,
                              font=font)
                    draw.text((1300, 900), f"Kills: {player2API['stats']['Blitz']['kills']:,}",
                              self.worse,
                              font=font)
                elif player1API['stats']['Blitz']['kills'] == player2API['stats']['Blitz']['kills']:
                    draw.text((0, 900), f"Kills: {player1API['stats']['Blitz']['kills']:,}",
                              self.same,
                              font=font)
                    draw.text((1300, 900), f"Kills: {player2API['stats']['Blitz']['kills']:,}",
                              self.same,
                              font=font)
                else:
                    draw.text((0, 900), f"Kills: {player1API['stats']['Blitz']['kills']:,}",
                              self.worse,
                              font=font)
                    draw.text((1300, 900), f"Kills: {player2API['stats']['Blitz']['kills']:,}",
                              self.better,
                              font=font)

                if player1API['stats']['Blitz']['deaths'] > player2API['stats']['Blitz']['deaths']:
                    draw.text((0, 1100), f"Deaths: {player1API['stats']['Blitz']['deaths']:,}",
                              self.better,
                              font=font)
                    draw.text((1300, 1100), f"Deaths: {player2API['stats']['Blitz']['deaths']:,}",
                              self.worse,
                              font=font)
                elif player1API['stats']['Blitz']['deaths'] == player2API['stats']['Blitz']['deaths']:
                    draw.text((0, 1100), f"Deaths: {player1API['stats']['Blitz']['deaths']:,}",
                              self.same,
                              font=font)
                    draw.text((1300, 1100), f"Deaths: {player2API['stats']['Blitz']['deaths']:,}",
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1100), f"Deaths: {player1API['stats']['Blitz']['deaths']:,}",
                              self.worse,
                              font=font)
                    draw.text((1300, 1100), f"Deaths: {player2API['stats']['Blitz']['deaths']:,}",
                              self.better,
                              font=font)

                if player1API['stats']['Blitz']['k_d'] > player1API['stats']['Blitz']['k_d']:
                    draw.text((0, 1300), f"KDR: {player1API['stats']['Blitz']['k_d']}",
                              self.better,
                              font=font)
                    draw.text((1300, 1300), f"KDR: {player2API['stats']['Blitz']['k_d']}",
                              self.worse,
                              font=font)
                elif player1API['stats']['Blitz']['k_d'] == player1API['stats']['Blitz']['k_d']:
                    draw.text((0, 1300), f"KDR: {player1API['stats']['Blitz']['k_d']}",
                              self.same,
                              font=font)
                    draw.text((1300, 1300), f"KDR: {player2API['stats']['Blitz']['k_d']}",
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1300), f"KDR: {player1API['stats']['Blitz']['k_d']}",
                              self.worse,
                              font=font)
                    draw.text((1300, 1300), f"KDR: {player2API['stats']['Blitz']['k_d']}",
                              self.better,
                              font=font)
                if player1API['stats']['Blitz']['win_loss'] > player2API['stats']['Blitz']['win_loss']:
                    draw.text((0, 1500), f"WLR: {player1API['stats']['Blitz']['win_loss']}",
                              self.better,
                              font=font)
                    draw.text((1300, 1500), f"WLR: {player2API['stats']['Blitz']['win_loss']}",
                              self.worse,
                              font=font)
                elif player1API['stats']['Blitz']['win_loss'] == player2API['stats']['Blitz']['win_loss']:
                    draw.text((0, 1500), f"WLR: {player1API['stats']['Blitz']['win_loss']}",
                              self.same,
                              font=font)
                    draw.text((1300, 1500), f"WLR: {player2API['stats']['Blitz']['win_loss']}",
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1500), f"WLR: {player1API['stats']['Blitz']['win_loss']}",
                              self.worse,
                              font=font)
                    draw.text((1300, 1500), f"WLR: {player2API['stats']['Blitz']['win_loss']}",
                              self.better,
                              font=font)

                if player1API['stats']['Blitz']['blitz_uses'] > player2API['stats']['Blitz']['blitz_uses']:
                    draw.text((0, 1700), f"Blitz Uses: {player1API['stats']['Blitz']['blitz_uses']:,}",
                              self.better,
                              font=font)
                    draw.text((1300, 1700), f"Blitz Uses: {player2API['stats']['Blitz']['blitz_uses']:,}",
                              self.worse,
                              font=font)
                elif player1API['stats']['Blitz']['blitz_uses'] == player2API['stats']['Blitz']['blitz_uses']:
                    draw.text((0, 1700), f"Blitz Uses: {player1API['stats']['Blitz']['blitz_uses']:,}",
                              self.same,
                              font=font)
                    draw.text((1300, 1700), f"Blitz Uses: {player2API['stats']['Blitz']['blitz_uses']:,}",
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1700), f"Blitz Uses: {player1API['stats']['Blitz']['blitz_uses']:,}",
                              self.worse,
                              font=font)
                    draw.text((1300, 1700), f"Blitz Uses: {player2API['stats']['Blitz']['blitz_uses']:,}",
                              self.better,
                              font=font)
                with io.BytesIO() as image_binary:
                    img.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))

            elif mode in ("skywars", 'sw'):
                img = Image.open("infoimgimg.png")
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("Minecraftia.ttf",
                                          65)
                fontbig = ImageFont.truetype("Minecraftia.ttf",
                                             250)
                draw.text((0, -100), "Skywars:", self.neutral, font=fontbig)

                draw.text((0, 400), f"Username:\n{player1}", self.neutral,
                          font=font)
                draw.text((1300, 400), f"Username:\n{player2}", self.neutral,
                          font=font)

                if player1API['stats']['SkyWars']['level'] > player2API['stats']['SkyWars']['level']:
                    draw.text((0, 700), f"Level: %.2f" % player1API['stats']['SkyWars']['level'],
                              self.better,
                              font=font)
                    draw.text((1300, 700), f"Level: %.2f" % player2API['stats']['SkyWars']['level'],
                              self.worse,
                              font=font)
                elif player1API['stats']['SkyWars']['level'] == player2API['stats']['SkyWars']['level']:
                    draw.text((0, 700), f"Level: %.2f" % player1API['stats']['SkyWars']['level'],
                              self.same,
                              font=font)
                    draw.text((1300, 700), f"Level: %.2f" % player2API['stats']['SkyWars']['level'],
                              self.same,
                              font=font)
                else:
                    draw.text((0, 700), f"Level: %.2f" % player1API['stats']['SkyWars']['level'],
                              self.worse,
                              font=font)
                    draw.text((1300, 700), f"Level: %.2f" % player2API['stats']['SkyWars']['level'],
                              self.better,
                              font=font)
                if player1API['stats']['SkyWars']['wins'] > player2API['stats']['SkyWars']['wins']:
                    draw.text((0, 900), f"Wins: {player1API['stats']['SkyWars']['wins']:,}",
                              self.better,
                              font=font)
                    draw.text((1300, 900), f"Wins: {player2API['stats']['SkyWars']['wins']:,}",
                              self.worse,
                              font=font)
                elif player1API['stats']['SkyWars']['wins'] == player2API['stats']['SkyWars']['wins']:
                    draw.text((0, 900), f"Wins: {player1API['stats']['SkyWars']['wins']:,}",
                              self.same,
                              font=font)
                    draw.text((1300, 900), f"Wins: {player2API['stats']['SkyWars']['wins']:,}",
                              self.same,
                              font=font)
                else:
                    draw.text((0, 900), f"Wins: {player1API['stats']['SkyWars']['wins']:,}",
                              self.worse,
                              font=font)
                    draw.text((1300, 900), f"Wins: {player2API['stats']['SkyWars']['wins']:,}",
                              self.better,
                              font=font)
                if player1API['stats']['SkyWars']['losses'] > player2API['stats']['SkyWars']['losses']:
                    draw.text((0, 1100), f"Losses: {player1API['stats']['SkyWars']['losses']:,}",
                              self.better,
                              font=font)
                    draw.text((1300, 1100), f"Losses: {player2API['stats']['SkyWars']['losses']:,}",
                              self.worse,
                              font=font)
                elif player1API['stats']['SkyWars']['losses'] == player2API['stats']['SkyWars']['losses']:
                    draw.text((0, 1100), f"Losses: {player1API['stats']['SkyWars']['losses']:,}",
                              self.same,
                              font=font)
                    draw.text((1300, 1100), f"Losses: {player2API['stats']['SkyWars']['losses']:,}",
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1100), f"Losses: {player1API['stats']['SkyWars']['losses']:,}",
                              self.worse,
                              font=font)
                    draw.text((1300, 1100), f"Losses: {player2API['stats']['SkyWars']['losses']:,}",
                              self.better,
                              font=font)

                if player1API['stats']['SkyWars']['win_loss_ratio'] > player2API['stats']['SkyWars']['win_loss_ratio']:
                    draw.text((0, 1300), f"WLR: {player1API['stats']['SkyWars']['win_loss_ratio']}",
                              self.better,
                              font=font)
                    draw.text((1300, 1300), f"WLR: {player2API['stats']['SkyWars']['win_loss_ratio']}",
                              self.worse,
                              font=font)
                elif player1API['stats']['SkyWars']['win_loss_ratio'] == player2API['stats']['SkyWars'][
                    'win_loss_ratio']:
                    draw.text((0, 1300), f"WLR: {player1API['stats']['SkyWars']['win_loss_ratio']}",
                              self.same,
                              font=font)
                    draw.text((1300, 1300), f"WLR: {player2API['stats']['SkyWars']['win_loss_ratio']}",
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1300), f"WLR: {player1API['stats']['SkyWars']['win_loss_ratio']}",
                              self.worse,
                              font=font)
                    draw.text((1300, 1300), f"WLR: {player2API['stats']['SkyWars']['win_loss_ratio']}",
                              self.better,
                              font=font)
                if player1API['stats']['SkyWars']['kills'] > player2API['stats']['SkyWars']['kills']:
                    draw.text((0, 1500), f"Kills: {player1API['stats']['SkyWars']['kills']:,}",
                              self.better,
                              font=font)
                    draw.text((1300, 1500), f"Kills: {player2API['stats']['SkyWars']['kills']:,}",
                              self.worse,
                              font=font)
                elif player1API['stats']['SkyWars']['kills'] == player2API['stats']['SkyWars']['kills']:
                    draw.text((0, 1500), f"Kills: {player1API['stats']['SkyWars']['kills']:,}",
                              self.same,
                              font=font)
                    draw.text((1300, 1500), f"Kills: {player2API['stats']['SkyWars']['kills']:,}",
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1500), f"Kills: {player1API['stats']['SkyWars']['kills']:,}",
                              self.worse,
                              font=font)
                    draw.text((1300, 1500), f"Kills: {player2API['stats']['SkyWars']['kills']:,}",
                              self.better,
                              font=font)

                if player1API['stats']['SkyWars']['deaths'] > player2API['stats']['SkyWars']['deaths']:
                    draw.text((0, 1700), f"Deaths: {player1API['stats']['SkyWars']['deaths']:,}",
                              self.better,
                              font=font)
                    draw.text((1300, 1700), f"Deaths: {player2API['stats']['SkyWars']['deaths']:,}",
                              self.worse,
                              font=font)
                elif player1API['stats']['SkyWars']['deaths'] == player2API['stats']['SkyWars']['deaths']:
                    draw.text((0, 1700), f"Deaths: {player1API['stats']['SkyWars']['deaths']:,}",
                              self.same,
                              font=font)
                    draw.text((1300, 1700), f"Deaths: {player2API['stats']['SkyWars']['deaths']:,}",
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1700), f"Deaths: {player1API['stats']['SkyWars']['deaths']:,}",
                              self.worse,
                              font=font)
                    draw.text((1300, 1700), f"Deaths: {player2API['stats']['SkyWars']['deaths']:,}",
                              self.better,
                              font=font)

                if player1API['stats']['SkyWars']['kill_death_ratio'] > player2API['stats']['SkyWars'][
                    'kill_death_ratio']:
                    draw.text((0, 1900), f"KDR: {player1API['stats']['SkyWars']['kill_death_ratio']}",
                              self.better,
                              font=font)
                    draw.text((1300, 1900), f"KDR: {player2API['stats']['SkyWars']['kill_death_ratio']}",
                              self.worse,
                              font=font)
                elif player1API['stats']['SkyWars']['kill_death_ratio'] == player2API['stats']['SkyWars'][
                    'kill_death_ratio']:
                    draw.text((0, 1900), f"KDR: {player1API['stats']['SkyWars']['kill_death_ratio']}",
                              self.same,
                              font=font)
                    draw.text((1300, 1900), f"KDR: {player2API['stats']['SkyWars']['kill_death_ratio']}",
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1900), f"KDR: {player1API['stats']['SkyWars']['kill_death_ratio']}",
                              self.worse,
                              font=font)
                    draw.text((1300, 1900), f"KDR: {player2API['stats']['SkyWars']['kill_death_ratio']}",
                              self.better,
                              font=font)

                with io.BytesIO() as image_binary:
                    img.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))

            elif mode in ("pit"):
                img = Image.open("infoimgimg.png")
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("Minecraftia.ttf",
                                          65)
                fontbig = ImageFont.truetype("Minecraftia.ttf",
                                             250)
                draw.text((0, -100), "PIT:", self.neutral, font=fontbig)

                draw.text((0, 400), f"Username:\n{player1}", self.neutral,
                          font=font)
                draw.text((1300, 400), f"Username:\n{player2}", self.neutral,
                          font=font)

                if player1API['stats']['Pit']['prestige'] > player2API['stats']['Pit']['prestige']:
                    draw.text((0, 700), f"Prestige: {player1API['stats']['Pit']['prestige']}",
                              self.better,
                              font=font)
                    draw.text((1300, 700), f"Prestige: {player2API['stats']['Pit']['prestige']}",
                              self.worse,
                              font=font)
                elif player1API['stats']['Pit']['prestige'] == player2API['stats']['Pit']['prestige']:
                    draw.text((0, 700), f"Prestige: {player1API['stats']['Pit']['prestige']}",
                              self.same,
                              font=font)
                    draw.text((1300, 700), f"Prestige: {player2API['stats']['Pit']['prestige']}",
                              self.same,
                              font=font)
                else:
                    draw.text((0, 700), f"Prestige: {player1API['stats']['Pit']['prestige']}",
                              self.worse,
                              font=font)
                    draw.text((1300, 700), f"Prestige: {player2API['stats']['Pit']['prestige']}",
                              self.better,
                              font=font)

                if player1API['stats']['Pit']['kills'] > player2API['stats']['Pit']['kills']:
                    draw.text((0, 900), f"Kills: {player1API['stats']['Pit']['kills']:,}",
                              self.better,
                              font=font)
                    draw.text((1300, 900), f"Kills: {player2API['stats']['Pit']['kills']:,}",
                              self.worse,
                              font=font)
                elif player1API['stats']['Pit']['kills'] == player2API['stats']['Pit']['kills']:
                    draw.text((0, 900), f"Kills: {player1API['stats']['Pit']['kills']:,}",
                              self.same,
                              font=font)
                    draw.text((1300, 900), f"Kills: {player2API['stats']['Pit']['kills']:,}",
                              self.same,
                              font=font)
                else:
                    draw.text((0, 900), f"Kills: {player1API['stats']['Pit']['kills']:,}",
                              self.worse,
                              font=font)
                    draw.text((1300, 900), f"Kills: {player2API['stats']['Pit']['kills']:,}",
                              self.better,
                              font=font)
                if player1API['stats']['Pit']['deaths'] > player2API['stats']['Pit']['deaths']:
                    draw.text((0, 1100), f"Deaths: {player1API['stats']['Pit']['deaths']:,}",
                              self.better,
                              font=font)
                    draw.text((1300, 1100), f"Deaths: {player2API['stats']['Pit']['deaths']:,}",
                              self.worse,
                              font=font)
                elif player1API['stats']['Pit']['deaths'] == player2API['stats']['Pit']['deaths']:
                    draw.text((0, 1100), f"Deaths: {player1API['stats']['Pit']['deaths']:,}",
                              self.same,
                              font=font)
                    draw.text((1300, 1100), f"Deaths: {player2API['stats']['Pit']['deaths']:,}",
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1100), f"Deaths: {player1API['stats']['Pit']['deaths']:,}",
                              self.worse,
                              font=font)
                    draw.text((1300, 1100), f"Deaths: {player2API['stats']['Pit']['deaths']:,}",
                              self.better,
                              font=font)

                if player1API['stats']['Pit']['kd_ratio'] > player2API['stats']['Pit']['kd_ratio']:
                    draw.text((0, 1300), f"KDR: {player1API['stats']['Pit']['kd_ratio']}",
                              self.better,
                              font=font)
                    draw.text((1300, 1300), f"KDR: {player2API['stats']['Pit']['kd_ratio']}",
                              self.worse,
                              font=font)
                elif player1API['stats']['Pit']['kd_ratio'] == player2API['stats']['Pit']['kd_ratio']:
                    draw.text((0, 1300), f"KDR: {player1API['stats']['Pit']['kd_ratio']}",
                              self.same,
                              font=font)
                    draw.text((1300, 1300), f"KDR: {player2API['stats']['Pit']['kd_ratio']}",
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1300), f"KDR: {player1API['stats']['Pit']['kd_ratio']}",
                              self.worse,
                              font=font)
                    draw.text((1300, 1300), f"KDR: {player2API['stats']['Pit']['kd_ratio']}",
                              self.better,
                              font=font)

                if player1API['stats']['Pit']['assists'] > player2API['stats']['Pit']['assists']:
                    draw.text((0, 1500), f"Assists: {player1API['stats']['Pit']['assists']:,}",
                              self.better,
                              font=font)
                    draw.text((1300, 1500), f"Assists: {player2API['stats']['Pit']['assists']:,}",
                              self.worse,
                              font=font)
                elif player1API['stats']['Pit']['assists'] == player2API['stats']['Pit']['assists']:
                    draw.text((0, 1500), f"Assists: {player1API['stats']['Pit']['assists']:,}",
                              self.same,
                              font=font)
                    draw.text((1300, 1500), f"Assists: {player2API['stats']['Pit']['assists']:,}",
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1500), f"Assists: {player1API['stats']['Pit']['assists']:,}",
                              self.worse,
                              font=font)
                    draw.text((1300, 1500), f"Assists: {player2API['stats']['Pit']['assists']:,}",
                              self.better,
                              font=font)

                if player1API['stats']['Pit']['max_streak'] > player2API['stats']['Pit']['max_streak']:
                    draw.text((0, 1700), f"Max streak: {player1API['stats']['Pit']['max_streak']:,}",
                              self.better,
                              font=font)
                    draw.text((1300, 1700), f"Max streak: {player2API['stats']['Pit']['max_streak']:,}",
                              self.worse,
                              font=font)
                elif player1API['stats']['Pit']['max_streak'] == player2API['stats']['Pit']['max_streak']:
                    draw.text((0, 1700), f"Max streak: {player1API['stats']['Pit']['max_streak']:,}",
                              self.same,
                              font=font)
                    draw.text((1300, 1700), f"Max streak: {player2API['stats']['Pit']['max_streak']:,}",
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1700), f"Max streak: {player1API['stats']['Pit']['max_streak']:,}",
                              self.worse,
                              font=font)
                    draw.text((1300, 1700), f"Max streak: {player2API['stats']['Pit']['max_streak']:,}",
                              self.better,
                              font=font)

                if player1API['stats']['Pit']['gold'] > player2API['stats']['Pit']['gold']:
                    draw.text((0, 1900), f"Gold: {player1API['stats']['Pit']['gold']:,}",
                              self.better,
                              font=font)
                    draw.text((1300, 1900), f"Gold: {player2API['stats']['Pit']['gold']:,}",
                              self.worse,
                              font=font)
                elif player1API['stats']['Pit']['gold'] == player2API['stats']['Pit']['gold']:
                    draw.text((0, 1900), f"Gold: {player1API['stats']['Pit']['gold']:,}",
                              self.same,
                              font=font)
                    draw.text((1300, 1900), f"Gold: {player2API['stats']['Pit']['gold']:,}",
                              self.same,
                              font=font)
                else:
                    draw.text((0, 1900), f"Gold: {player1API['stats']['Pit']['gold']:,}",
                              self.worse,
                              font=font)
                    draw.text((1300, 1900), f"Gold: {player2API['stats']['Pit']['gold']:,}",
                              self.better,
                              font=font)

                with io.BytesIO() as image_binary:
                    img.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))

            else:
                img = Image.open("infoimgimg.png")
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("Minecraftia.ttf",
                                          80)
                fontbig = ImageFont.truetype("Minecraftia.ttf",
                                             200)
                draw.text((0, 0), "Invalid Mode", (255, 0, 0), font=fontbig)

                draw.text((0, 300), "Valid Mods:", (0, 255, 0), font=font)

                draw.text((0, 500), "Overall", (0, 255, 0), font=font)

                draw.text((0, 700), "Bedwars", (0, 255, 0), font=font)
                draw.text((0, 850), "Bedwars_solo", (0, 255, 0), font=font)
                draw.text((0, 1000), "Bedwars_doubles", (0, 255, 0), font=font)
                draw.text((0, 1150), "Bedwars_threes", (0, 255, 0), font=font)
                draw.text((0, 1300), "Bedwars_fours", (0, 255, 0), font=font)

                draw.text((0, 1500), "duels", (0, 255, 0), font=font)

                draw.text((0, 1650), "blitz", (0, 255, 0), font=font)

                draw.text((0, 1800), "skywars", (0, 255, 0), font=font)

                draw.text((1500, 500), "Pit", (0, 255, 0), font=font)

                with io.BytesIO() as image_binary:
                    img.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))

    @commands.command(name="compare_users", aliases=["compare_user"], description="Get discord user stats")
    async def compare_users(self, ctx, user1: discord.User = None, user2: discord.User = None):
        if user2 is None and user1 is not None:
            user2 = user1
            user1 = ctx.author
            print(user1)
            print(user2)
        if user1 is None:
            await ctx.send("You need to provide atleast one user(either the id or tag them)")
            return
        img = Image.open("infoimgimg.png")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("Minecraftia.ttf",
                                  80)
        fontbig = ImageFont.truetype("Minecraftia.ttf",
                                     190)
        draw.text((0, 0), "Discord User Stats:", (255, 255, 255), font=fontbig)
        draw.text((0, 400), f"Name:\n{user1}", self.neutral,
                  font=font)
        draw.text((1300, 400), f"Name:\n{user2}", self.neutral,
                  font=font)
        Cdays1 = (datetime.datetime.utcnow() - user1.created_at).days
        Cdays2 = (datetime.datetime.utcnow() - user2.created_at).days
        if user1.created_at < user2.created_at:
            draw.text((0, 700),
                      f"Account created:\n{user1.created_at.strftime('%d %b %Y %H:%M')}\n(Days: {Cdays1})",
                      self.better,
                      font=font)
            draw.text((1300, 700),
                      f"Account created:\n{user2.created_at.strftime('%d %b %Y %H:%M')}\n(Days: {Cdays2})",
                      self.worse,
                      font=font)
        elif user1.created_at == user2.created_at:
            draw.text((0, 700),
                      f"Account created:\n{user1.created_at.strftime('%d %b %Y %H:%M')}\n(Days: {Cdays1})",
                      self.neutral,
                      font=font)
            draw.text((1300, 700),
                      f"Account created:\n{user2.created_at.strftime('%d %b %Y %H:%M')}\n(Days: {Cdays2})",
                      self.neutral,
                      font=font)
        else:
            draw.text((0, 700),
                      f"Account created:\n{user1.created_at.strftime('%d %b %Y %H:%M')}\n(Days: {Cdays1})",
                      self.worse,
                      font=font)
            draw.text((1300, 700),
                      f"Account created:\n{user2.created_at.strftime('%d %b %Y %H:%M')}\n(Days: {Cdays2})",
                      self.better,
                      font=font)
        guild = self.bot.get_guild(ctx.guild.id)
        if guild.get_member(user1.id) and guild.get_member(user2.id):
            member1: discord.Member = await guild.fetch_member(user1.id)
            member2: discord.Member = await guild.fetch_member(user2.id)
            days1 = (datetime.datetime.utcnow() - member1.joined_at).days
            days2 = (datetime.datetime.utcnow() - member2.joined_at).days
            if days1 > days2:
                draw.text((0, 1100),
                          f"Joined at:\n{member1.joined_at.strftime('%d %b %Y ')}\n(Days: {days1})",
                          self.better,
                          font=font)
                draw.text((1300, 1100),
                          f"Joined at:\n{member2.joined_at.strftime('%d %b %Y ')}\n(Days: {days2})",
                          self.worse,
                          font=font)
            elif days1 == days2:
                draw.text((0, 1100),
                          f"Joined at:\n{member1.joined_at.strftime('%d %b %Y ')}\n(Days: {days1})",
                          self.neutral,
                          font=font)
                draw.text((1300, 1100),
                          f"Joined at:\n{member2.joined_at.strftime('%d %b %Y ')}\n(Days: {days2})",
                          self.neutral,
                          font=font)
            else:
                draw.text((0, 1100),
                          f"Joined at:\n{member1.joined_at.strftime('%d %b %Y ')}\n(Days: {days1})",
                          self.worse,
                          font=font)
                draw.text((1300, 1100),
                          f"Joined at:\n{member2.joined_at.strftime('%d %b %Y ')}\n(Days: {days2})",
                          self.better,
                          font=font)
            if member1.top_role > member2.top_role:
                draw.text((0, 1500),
                          f"Top Role:\n{member1.top_role}",
                          self.better,
                          font=font)
                draw.text((1300, 1500),
                          f"Top Role:\n{member2.top_role}",
                          self.worse,
                          font=font)
            elif member1.top_role == member2.top_role:
                draw.text((0, 1500),
                          f"Top Role:\n{member1.top_role}",
                          self.neutral,
                          font=font)
                draw.text((1300, 1500),
                          f"Top Role:\n{member2.top_role}",
                          self.neutral,
                          font=font)
            else:
                draw.text((0, 1500),
                          f"Top Role:\n{member1.top_role}",
                          self.worse,
                          font=font)
                draw.text((1300, 1500),
                          f"Top Role:\n{member2.top_role}",
                          self.better,
                          font=font)
            with io.BytesIO() as image_binary:
                img.save(image_binary, 'PNG')
                image_binary.seek(0)
                await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))
            return
        if guild.get_member(user1.id) is None and guild.get_member(user2.id) is None:
            draw.text((0, 1100),
                      f"Not In Server:\nThis Person isnt \nin this server",
                      self.worse,
                      font=font)
            draw.text((1300, 1100),
                      f"Not In Server:\nThis Person isnt \nin this server",
                      self.worse,
                      font=font)
            with io.BytesIO() as image_binary:
                img.save(image_binary, 'PNG')
                image_binary.seek(0)
                await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))
            return
        if guild.get_member(user1.id) is None:
            member2: discord.Member = await guild.fetch_member(user2.id)
            days2 = (datetime.datetime.utcnow() - member2.joined_at).days
            draw.text((0, 1100),
                      f"Not In Server:\nThis Person isnt \nin this server",
                      self.worse,
                          font=font)
            draw.text((1300, 1100),
                          f"Joined at:\n{member2.joined_at.strftime('%d %b %Y ')}\n(Days: {days2})",
                          self.better,
                          font=font)

            draw.text((1300, 1500),
                          f"Top Role:\n{member2.top_role}",
                          self.better,
                          font=font)
            with io.BytesIO() as image_binary:
                img.save(image_binary, 'PNG')
                image_binary.seek(0)
                await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))
            return
        if guild.get_member(user2.id) is None:
            member1: discord.Member = await guild.fetch_member(user1.id)
            days1 = (datetime.datetime.utcnow() - member1.joined_at).days
            draw.text((1300, 1100),
                      f"Not In Server:\nThis Person isnt \nin this server",
                      self.worse,
                      font=font)
            draw.text((0, 1100),
                      f"Joined at:\n{member1.joined_at.strftime('%d %b %Y ')}\n(Days: {days1})",
                      self.better,
                      font=font)

            draw.text((0, 1500),
                      f"Top Role:\n{member1.top_role}",
                      self.better,
                      font=font)
            with io.BytesIO() as image_binary:
                img.save(image_binary, 'PNG')
                image_binary.seek(0)
                await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))
            return


def setup(bot):
    bot.add_cog(Compare(bot))

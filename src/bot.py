# Description: A Discord bot that sends server information to a channel every minute.
# Author: < ᵈᵉᵛZen />
# Version: 1.0
# Date: 2023-02-20
# License: MIT
# Requirements: discord.py, discord.py.ext.tasks
# Usage: python src/bot.py


import a2s
from datetime import datetime
import discord
from discord.ext import tasks, commands
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))
SERVER_IP = os.getenv('SERVER_IP')
SERVER_PORT = int(os.getenv('SERVER_PORT'))

intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='!', intents=intents)

last_message = None  # Variable to store the last message sent

def format_players(player_list):
    if not player_list:
        return "No Players Online."

    players_per_column = len(player_list) // 2 + (len(player_list) % 2)
    col1 = player_list[:players_per_column]
    col2 = player_list[players_per_column:]

    max_name_length = max(len(p.name) for p in player_list) + 2
    space_between = " " * 5

    formatted_list = "\n".join(
        f"{p1.name.ljust(max_name_length)}{space_between}{p2.name.ljust(max_name_length)}" if p2 else
        f"{p1.name.ljust(max_name_length)}"
        for p1, p2 in zip(col1, col2 + [None])
    )

    return formatted_list

def get_server_info():
    try:
        server_address = (SERVER_IP, SERVER_PORT)
        server_info = a2s.info(server_address)
        player_list = a2s.players(server_address)

        server_name = server_info.server_name
        game_map = server_info.map_name
        max_players = server_info.max_players
        player_count = len(player_list)

        players = format_players(player_list)

        embed = discord.Embed(title=f"🌍 Host Server : **{server_name}**", color=0x2ecc71)
        embed.add_field(name="🗺 Current Map", value=game_map, inline=True)
        embed.add_field(name="👥 Players Connected", value=f"{player_count}/{max_players} - Players", inline=True)
        embed.add_field(name="📌 Server IP", value=f":arrow_right: {SERVER_IP}:{SERVER_PORT}", inline=True)
        embed.add_field(name="🎮 Players Online List", value=f"```\n{players}\n```", inline=False)
        embed.set_footer(text=f"Server Update Time • {datetime.now().strftime('%H:%M:%S')}", icon_url="https://cdn.discordapp.com/attachments/1006072849888464968/1279389095591940219/nationz.gif")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1072023091330428948/1279371158621524051/nation.gif")

        return embed
    except Exception as e:
        embed = discord.Embed(title="⚠ Error", description=f"Error retrieving data from server: {e}", color=0xe74c3c)
        return embed

@tasks.loop(minutes=1)
async def send_to_discord():
    global last_message  # declareLastMessageComoGlobal
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        embed = get_server_info()
        # await channel.send(embed=embed)
        if last_message:
            try:
                await last_message.delete()
            except discord.errors.NotFound:
                pass  # The message has already been deleted
        last_message = await channel.send(embed=embed)

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')
    send_to_discord.start()

bot.run(TOKEN)
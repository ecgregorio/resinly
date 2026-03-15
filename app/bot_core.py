import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

from tasks import (
    resin_loop,
)

#  bot init/events
# handles bot creation, intents, logging, and event registration

# Consts
COOKIE_GUIDE_URL = "https://github.com/ecgregorio/resinly#finding-your-hoyolab-cookies"

# load .env file
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
default_genshin_uid = os.getenv('GENSHIN_UID')
check_interval_seconds = int(os.getenv('CHECK_INTERVAL_SECONDS', '300')) # 2nd param is default

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()

# specify manual intents
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

### ---- Events ---- ###
@bot.event
async def on_ready():
    if bot.user is None: # guard check
        return
    print(f"We are ready to go in, {bot.user.name}")

    await bot.change_presence(status=discord.Status.idle, activity=discord.CustomActivity(name="/setup | !resin"))
    
    # sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s).")
    except Exception as e:
        print(f"Slash sync failed: {type(e).__name__}")
    
    if not resin_loop.is_running():
        resin_loop.start()

import logging
from dotenv import load_dotenv
import os

from app.bot_core import bot

# load .env file
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# handler
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# token guard
if token is None:
    raise RuntimeError("DISCORD_TOKEN is not set in .env")

# authenticate and start the bot
bot.run(token, log_handler=handler, log_level=logging.INFO)
import logging

from interactions import Client, Intents, listen, slash_command, SlashContext
import json

with open("app_credentials.json") as file:
    token_json = json.load(file)

bot_token = token_json["bot_token"]

logging.basicConfig()
cls_log = logging.getLogger("SLBotLogger")
cls_log.setLevel(logging.DEBUG)

bot = Client(
    intents=Intents.DEFAULT,
    logger=cls_log)

@listen()  
async def on_ready():
    print("Ready")
    print(f"This bot is owned by {bot.owner}")

@slash_command(name="reload")
async def reload(ctx: SlashContext):
    bot.reload_extension("commands.BaseCommands")

bot.load_extension("commands.BaseCommands")
bot.start(bot_token)
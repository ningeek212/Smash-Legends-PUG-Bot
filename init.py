import logging

from interactions import (
    Client, Intents, listen, slash_command, SlashContext, BaseChannel, ChannelType,
    GuildText
)
import json
from utils import spreadsheet
from utils.config import DEV_TASK_CHANNEL_ID
from tasks.GameSignupTasks import GameSignupTasks

with open("credentials/app_credentials.json") as file:
    token_json = json.load(file)

bot_token = token_json["bot_token"]

logging.basicConfig()
cls_log = logging.getLogger("SLBotLogger")
cls_log.setLevel(logging.DEBUG)

bot = Client(
    intents=Intents.DEFAULT,
    logger=cls_log)

spreadsheet.setup()

@listen()  
async def on_ready() -> None:
    print("Starting game tasks")
    channel: BaseChannel = bot.get_channel(DEV_TASK_CHANNEL_ID)
    if not channel or not channel.type == ChannelType.GUILD_TEXT:
        bot.logger.error("Could not retrieve dev channel")
        print("Failed to start game tasks")
    else:
        channel: GuildText = channel
        games: GameSignupTasks= bot.get_ext("tasks.GameSignupTasks")
        games.add_channel(channel)
        print("Successfully started game tasks")
    print("Ready")
    print(f"This bot is owned by {bot.owner}")

@slash_command(name="reload")
async def reload(ctx: SlashContext) -> None:
    bot.reload_extension("commands.BaseCommands")
    bot.reload_extension("commands.GameCommands")
    bot.load_extension("tasks.GameSignupTasks")
    # bot.reload_extension("commands.TaskCommands")
    await ctx.send("Reload")

bot.load_extension("commands.BaseCommands")
bot.load_extension("commands.GameCommands")
bot.load_extension("tasks.GameSignupTasks")
# bot.load_extension("commands.TaskCommands")
bot.start(bot_token)
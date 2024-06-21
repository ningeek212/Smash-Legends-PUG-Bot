from interactions import Client, Intents, listen, slash_command, SlashContext
import json

with open("app_credentials.json") as file:
    token_json = json.load(file)

bot_token = token_json["bot_token"]

bot = Client(intents=Intents.DEFAULT)
# intents are what events we want to receive from discord, `DEFAULT` is usually fine

@listen()  # this decorator tells snek that it needs to listen for the corresponding event, and run this coroutine
async def on_ready():
    # This event is called when the bot is ready to respond to commands
    print("Ready")
    print(f"This bot is owned by {bot.owner}")

bot.load_extension("commands.BaseCommands")
bot.start(bot_token)
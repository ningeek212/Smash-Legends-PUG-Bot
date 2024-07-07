from interactions import (
    slash_command, slash_option, SlashContext, SlashCommandChoice, Extension, OptionType,
    Client
)
from asyncio import create_task
from utils.enums import Gamemode
from utils.utils import create_pages
from utils.const import COMMAND_PERMISSIONS
from utils.spreadsheet import get_dominion_elo, get_duo_elo, get_duel_elo
from games.GameSignupManager import GameSignupManager


class GameCommands(Extension):
    def __init__(self, bot: Client) -> None:
        self.bot = bot
        self.game_manager: GameSignupManager = None
    
    def add_signup_manager(self, game_manager: GameSignupManager) -> None:
        self.game_manager = game_manager

    @slash_command(
        name="elo",
        description="List the rankings of players for a gamemode according to their elo"
        )
    @slash_option(
        name="gamemode",
        opt_type=OptionType.INTEGER,
        required=True,
        description="Which gamemode you want to see the players' elo",
        choices=[
            SlashCommandChoice("Dominion", Gamemode.DOMINION.value),
            SlashCommandChoice("Duo", Gamemode.DUO.value),
            SlashCommandChoice("Duel", Gamemode.DUEL.value)
        ]
    )
    async def elo_function(self, ctx: SlashContext, gamemode: int) -> None:
        mode = Gamemode(gamemode)
        match mode:
            case Gamemode.DOMINION:
                data = get_dominion_elo()
            case Gamemode.DUO:
                data = get_duo_elo()
            case Gamemode.DUEL:
                data = get_duel_elo()
        
        sorted_data = sorted(data, key=lambda elo: elo[1], reverse=True)
        data_str = [str(elo).ljust(5, ' ') + '\t' + player for (player, elo) in sorted_data]
        await create_pages(ctx, f"{mode.name} Elo", data_str, page_title="Elo: \t Player:")

    @slash_command(
        name="channel_game_signups",
        description="Get a list of all channels currently running game signups",
        default_member_permissions=COMMAND_PERMISSIONS["TASK_LOOP"]
    )
    async def channel_game_signups_function(self, ctx: SlashContext) -> None:
        game_list: list[str] = []
        for game in self.game_manager.games.values():
            game_list.append(f"<#{game.channel.id}>")
        await create_pages(
            ctx, "Game signup tasks", game_list,
            if_empty="No channels currently running game signups"
        )

        
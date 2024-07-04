from interactions import slash_command, slash_option, SlashContext, SlashCommandChoice, Extension
from interactions import OptionType
from utils.enums import Gamemode
from utils.utils import create_pages
from utils.spreadsheet import get_dominion_elo, get_duo_elo, get_duel_elo


class GameCommands(Extension):
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
    async def elo_function(self, ctx: SlashContext, gamemode: int):
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


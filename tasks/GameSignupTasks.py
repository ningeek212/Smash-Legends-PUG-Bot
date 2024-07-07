from interactions import (
    Client, GuildText, component_callback, ComponentContext, Embed, Member, Extension, 
    Snowflake
)
from typing import Callable
from utils.enums import TaskType
from utils.utils import signup_list_to_string, error_embed
from tasks.GameSignup import GameSignup

type Games = dict[Snowflake, GameSignup]


class GameSignupTasks(Extension):
    def __init__(self, bot: Client) -> None:
        self.bot = bot
        self.games: Games = {}
    
    def add_channel(self, channel: GuildText) -> GameSignup:
        if channel.id in self.games.keys():
            # TODO: Add error
            return
        new_game = GameSignup(self.bot, channel)
        self.games[channel.id] = new_game
        
    # Join Dominion button

    @component_callback("join_dom")
    async def join_dom_callback(self, ctx: ComponentContext) -> None:
        game: GameSignup = self.games.get(ctx.channel_id)
        if game is None:
            await error_embed(ctx, description="Tried joining a game with no task loop")
            # TODO: Add error
            return

        joining_member: Member = ctx.author
        print(f"joining member: {joining_member.display_name}")
        if joining_member in game.dominion_signups:
            # TODO: Send message about player already joined
            return
        
        game.dominion_signups[game.num_dom_signups] = joining_member
        game.num_dom_signups += 1
        signup_str: str = signup_list_to_string(game.dominion_signups)
        print(signup_str)
        embed = Embed(
            title="Dominion PUG (3v3)",
            description=signup_str,
            footer=f"({game.num_dom_signups}/6)"
        )
        await game.dominion_message.edit(embed=embed)

        if game.num_dom_signups == 6:
            # TODO: start game with signups
            game.dominion_task.restart()
        elif game.num_dom_signups > 6:
            await error_embed(ctx, "Uh-oh! More than 6 people signed up! How'd that happen")
    
    # Leave Dominion button

    @component_callback("leave_dom")
    async def leave_dom_callback(self, ctx: ComponentContext) -> None:
        game: GameSignup = self.games.get(ctx.channel_id)
        if game is None:
            await error_embed(ctx, description="Tried joining a game with no task loop")
            # TODO: Add error
            return

        leaving_member: Member = ctx.author
        print(f"joining member: {leaving_member.display_name}")
        if not leaving_member in game.dominion_signups:
            # TODO: Add message saying player already left
            return
        
        game.dominion_signups.remove(leaving_member)
        game.dominion_signups.append(None)
        game.num_dom_signups -= 1
        signup_str: str = signup_list_to_string(game.dominion_signups)
        print(signup_str)
        embed = Embed(
            title="Dominion PUG (3v3)",
            description=signup_str,
            footer=f"({game.num_dom_signups}/6)"
        )
        await game.dominion_message.edit(embed=embed)

    # Join Duo button

    @component_callback("join_duo")
    async def join_duo_callback(self, ctx: ComponentContext) -> None:
        game: GameSignup = self.games.get(ctx.channel_id)
        if game is None:
            await error_embed(ctx, description="Tried joining a game with no task loop")
            # TODO: Add error
            return

        joining_member: Member = ctx.author
        print(f"joining member: {joining_member.display_name}")
        if joining_member in game.duo_signups:
            # TODO: Send message about player already joined
            return
        
        game.duo_signups[game.num_duo_signups] = joining_member
        game.num_duo_signups += 1
        signup_str: str = signup_list_to_string(game.duo_signups)
        print(signup_str)
        embed = Embed(
            title="Duo PUG (2v2)",
            description=signup_str,
            footer=f"({game.num_duo_signups}/4)"
        )
        await game.duo_message.edit(embed=embed)

        if game.num_duo_signups == 4:
            # TODO: start game with signups
            game.duo_task.restart()
        elif game.num_duo_signups > 4:
            await error_embed(ctx, "Uh-oh! More than 4 people signed up! How'd that happen")
    
    # Leave Duo button

    @component_callback("leave_duo")
    async def leave_duo_callback(self, ctx: ComponentContext) -> None:
        game: GameSignup = self.games.get(ctx.channel_id)
        if game is None:
            await error_embed(ctx, description="Tried joining a game with no task loop")
            # TODO: Add error
            return

        leaving_member: Member = ctx.author
        print(f"joining member: {leaving_member.display_name}")
        if not leaving_member in game.duo_signups:
            # TODO: Add message saying player already left
            return
        
        game.duo_signups.remove(leaving_member)
        game.duo_signups.append(None)
        game.num_duo_signups -= 1
        signup_str: str = signup_list_to_string(game.duo_signups)
        print(signup_str)
        embed = Embed(
            title="Duo PUG (2v2)",
            description=signup_str,
            footer=f"({game.num_duo_signups}/4)"
        )
        await game.duo_message.edit(embed=embed)

    # Join Duel button

    @component_callback("join_duel")
    async def join_duel_callback(self, ctx: ComponentContext) -> None:
        game: GameSignup = self.games.get(ctx.channel_id)
        if game is None:
            await error_embed(ctx, description="Tried joining a game with no task loop")
            # TODO: Add error
            return

        joining_member: Member = ctx.author
        print(f"joining member: {joining_member.display_name}")
        if joining_member in game.duel_signups:
            # TODO: Send message about player already joined
            return
        
        game.duel_signups[game.num_duel_signups] = joining_member
        game.num_duel_signups += 1
        signup_str: str = signup_list_to_string(game.duel_signups)
        print(signup_str)
        embed = Embed(
            title="Duel PUG (1v1)",
            description=signup_str,
            footer=f"({game.num_duel_signups}/2)"
        )
        await game.duel_message.edit(embed=embed)

        if game.num_duel_signups == 2:
            # TODO: start game with signups
            game.duel_task.restart()
        elif game.num_duel_signups > 4:
            await error_embed(ctx, "Uh-oh! More than 2 people signed up! How'd that happen")
    
    # Leave Duo button

    @component_callback("leave_duel")
    async def leave_duel_callback(self, ctx: ComponentContext) -> None:
        game: GameSignup = self.games.get(ctx.channel_id)
        if game is None:
            await error_embed(ctx, description="Tried joining a game with no task loop")
            # TODO: Add error
            return

        leaving_member: Member = ctx.author
        print(f"joining member: {leaving_member.display_name}")
        if not leaving_member in game.duel_signups:
            # TODO: Add message saying player already left
            return
        
        game.duel_signups.remove(leaving_member)
        game.duel_signups.append(None)
        game.num_duel_signups -= 1
        signup_str: str = signup_list_to_string(game.duel_signups)
        print(signup_str)
        embed = Embed(
            title="Duel PUG (1v1)",
            description=signup_str,
            footer=f"({game.num_duel_signups}/2)"
        )
        await game.duel_message.edit(embed=embed)


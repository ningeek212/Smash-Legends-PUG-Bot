from __future__ import annotations
from typing import TYPE_CHECKING
from asyncio import create_task

from interactions import (
    Client, GuildText, component_callback, ComponentContext, Embed, Member, Extension
)

from utils.utils import signup_list_to_string, error_embed
from utils.enums import SignupState
from games.GameSignup import GameSignup

if TYPE_CHECKING:
    from utils.types import GameSignups


class GameSignupManager(Extension):
    def __init__(self, bot: Client) -> None:
        self.bot = bot
        self.games: GameSignups = {}
    
    def drop(self):
        create_task(self.async_drop())
        super().drop()
    
    async def async_drop(self):
        for game in self.games.values():
            await game.stop()
    
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
        
        if game.dom_signup_state == SignupState.Launching:
            return

        joining_member: Member = ctx.author
        if game.is_member_signed(joining_member):
            # TODO: Send message about player already signed up
            return
        
        game.dominion_signups[game.num_dom_signups] = joining_member
        game.num_dom_signups += 1
        signup_str: str = signup_list_to_string(game.dominion_signups)
        embed = Embed(
            title="Dominion PUG (3v3)",
            description=signup_str,
            footer=f"({game.num_dom_signups}/6)"
        )
        await ctx.edit_origin(embed=embed)

        if game.num_dom_signups == 6:
            game.dom_signup_state = SignupState.Launching
            # TODO: start game with signups
            game.dom_signup_state = SignupState.Started
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
        
        if game.dom_signup_state == SignupState.Launching:
            return

        leaving_member: Member = ctx.author
        if not leaving_member in game.dominion_signups:
            # TODO: Add message saying player already left
            return
        
        game.dominion_signups.remove(leaving_member)
        game.dominion_signups.append(None)
        game.num_dom_signups -= 1
        signup_str: str = signup_list_to_string(game.dominion_signups)
        embed = Embed(
            title="Dominion PUG (3v3)",
            description=signup_str,
            footer=f"({game.num_dom_signups}/6)"
        )
        await ctx.edit_origin(embed=embed)

    # Join Duo button

    @component_callback("join_duo")
    async def join_duo_callback(self, ctx: ComponentContext) -> None:
        game: GameSignup = self.games.get(ctx.channel_id)
        if game is None:
            await error_embed(ctx, description="Tried joining a game with no task loop")
            # TODO: Add error
            return

        if game.duo_signup_state == SignupState.Launching:
            return

        joining_member: Member = ctx.author
        if joining_member in game.duo_signups:
            # TODO: Send message about player already joined
            return
        
        game.duo_signups[game.num_duo_signups] = joining_member
        game.num_duo_signups += 1
        signup_str: str = signup_list_to_string(game.duo_signups)
        embed = Embed(
            title="Duo PUG (2v2)",
            description=signup_str,
            footer=f"({game.num_duo_signups}/4)"
        )
        await ctx.edit_origin(embed=embed)

        if game.num_duo_signups == 4:
            game.duo_signup_state = SignupState.Launching
            # TODO: start game with signups
            game.duo_signup_state = SignupState.Started
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
        
        if game.duo_signup_state == SignupState.Launching:
            return

        leaving_member: Member = ctx.author
        if not leaving_member in game.duo_signups:
            # TODO: Add message saying player already left
            return
        
        game.duo_signups.remove(leaving_member)
        game.duo_signups.append(None)
        game.num_duo_signups -= 1
        signup_str: str = signup_list_to_string(game.duo_signups)
        embed = Embed(
            title="Duo PUG (2v2)",
            description=signup_str,
            footer=f"({game.num_duo_signups}/4)"
        )
        await ctx.edit_origin(embed=embed)

    # Join Duel button

    @component_callback("join_duel")
    async def join_duel_callback(self, ctx: ComponentContext) -> None:
        game: GameSignup = self.games.get(ctx.channel_id)
        if game is None:
            await error_embed(ctx, description="Tried joining a game with no task loop")
            # TODO: Add error
            return
        
        if game.duel_signup_state == SignupState.Launching:
            return

        joining_member: Member = ctx.author
        if joining_member in game.duel_signups:
            # TODO: Send message about player already joined
            return
        
        game.duel_signups[game.num_duel_signups] = joining_member
        game.num_duel_signups += 1
        signup_str: str = signup_list_to_string(game.duel_signups)
        embed = Embed(
            title="Duel PUG (1v1)",
            description=signup_str,
            footer=f"({game.num_duel_signups}/2)"
        )
        await ctx.edit_origin(embed=embed)

        if game.num_duel_signups == 2:
            game.duel_signup_state = SignupState.Launching
            # TODO: start game with signups
            game.duel_signup_state = SignupState.Started
            game.duel_task.restart()
        elif game.num_duel_signups > 2:
            await error_embed(ctx, "Uh-oh! More than 2 people signed up! How'd that happen")
    
    # Leave Duo button

    @component_callback("leave_duel")
    async def leave_duel_callback(self, ctx: ComponentContext) -> None:
        game: GameSignup = self.games.get(ctx.channel_id)
        if game is None:
            await error_embed(ctx, description="Tried joining a game with no task loop")
            # TODO: Add error
            return
        
        if game.duel_signup_state == SignupState.Launching:
            return

        leaving_member: Member = ctx.author
        if not leaving_member in game.duel_signups:
            # TODO: Add message saying player already left
            return
        
        game.duel_signups.remove(leaving_member)
        game.duel_signups.append(None)
        game.num_duel_signups -= 1
        signup_str: str = signup_list_to_string(game.duel_signups)
        embed = Embed(
            title="Duel PUG (1v1)",
            description=signup_str,
            footer=f"({game.num_duel_signups}/2)"
        )
        await ctx.edit_origin(embed=embed)


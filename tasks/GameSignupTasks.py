from interactions import (
    Client, GuildText, Task, BaseTrigger, IntervalTrigger, component_callback, ComponentContext,
    Embed, Message, Button, ButtonStyle, ActionRow, Member, spread_to_rows, Extension, Snowflake
)
from typing import Callable
from utils.enums import TaskType
from utils.utils import Signups, signup_list_to_string, error_embed
from utils.config import GAME_SIGNUP_INTERVAL

type Games = dict[Snowflake, GameSignup]

class GameTask(Task):
    def __init__(self, callback: Callable, trigger: BaseTrigger, task_type: TaskType) -> None:
        self.task_type: TaskType = task_type
        super().__init__(callback, trigger)


class GameSignup():

    def __init__(self, bot: Client, channel: GuildText) -> None:
        self.bot = bot
        self.channel = channel
        self.active: bool = True

        # Dominion setup
        self.dominion_task: GameTask = None
        self.dominion_message: Message = None
        self.dominion_signups: Signups = [None for i in range(6)]
        self.num_dom_signups: int = 0
        if not channel is None:
            self._start_dominion_loop()

        # Duo setup
        self.duo_task: GameTask = None

        # Duel setup
        self.duel_task: GameTask = None

    async def start(self) -> None:
        if self.active:
            self.bot.logger.warn("Tried starting signup task loop, but was already started")
            return
        self._start_dominion_loop()
        # self._start_duo_loop()
        # self._start_duel_loop()
        self.active = True
    
    async def stop(self) -> None:
        if not self.active:
            self.bot.logger.warn("Tried stopping signup task loop, but was already stopped")
            return
        self.dominion_task.stop()
        self.active = False

    def _start_dominion_loop(self):

        #========================================================================
        async def dominion_loop():
            if self.dominion_message:
                await self._restart_dominion_loop()
            
            signup_str: str = signup_list_to_string(self.dominion_signups)
            embed = Embed(
                title="Dominion PUG (3v3)",
                description=signup_str,
                footer=f"({self.num_dom_signups}/6)"
            )

            join_button = Button(
                style=ButtonStyle.GREEN,
                label="Join",
                custom_id="join_dom"
            )
            leave_button = Button(
                style=ButtonStyle.RED,
                label="Leave",
                custom_id="leave_dom"
            )
            button_row: list[ActionRow] = spread_to_rows(join_button, leave_button)

            self.dominion_message = await self.channel.send(embed=embed, components=button_row)
        #========================================================================
        
        self.dominion_task = GameTask(
            dominion_loop,
            IntervalTrigger(minutes=GAME_SIGNUP_INTERVAL),
            TaskType.DOMINION
        )
        self.dominion_task.start()

    async def _restart_dominion_loop(self):
        self.dominion_signups = [None for i in range(6)]
        self.num_dom_signups = 0
        await self.dominion_message.delete()


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
        
    # Join button

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
            # start game with signups
            game.dominion_task.restart()
        elif game.num_dom_signups > 6:
            await error_embed(ctx, "Uh-oh! More than 6 people signed up! How'd that happen")
    
    # Leave button

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


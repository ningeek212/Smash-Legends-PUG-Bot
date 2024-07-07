from interactions import (
    Client, GuildText, Task, Message, Embed, Button, ButtonStyle, ActionRow, IntervalTrigger,
    Member, spread_to_rows
)
from utils.utils import signup_list_to_string, Signups
from utils.const import GAME_SIGNUP_INTERVAL


class GameSignup():

    def __init__(self, bot: Client, channel: GuildText) -> None:
        self.bot = bot
        self.channel = channel
        self.active: bool = True

        # Dominion setup
        self.dominion_task: Task = None
        self.dominion_message: Message = None
        self.dominion_signups: Signups = [None for i in range(6)]
        self.num_dom_signups: int = 0

        # Duo setup
        self.duo_task: Task = None
        self.duo_message: Message = None
        self.duo_signups: Signups = [None for i in range(4)]
        self.num_duo_signups: int = 0

        # Duel setup
        self.duel_task: Task = None
        self.duel_message: Message = None
        self.duel_signups: Signups = [None for i in range(2)]
        self.num_duel_signups: int = 0

        if not channel is None:
            self._start_dominion_loop()
            self._start_duo_loop()
            self._start_duel_loop()

    async def start(self) -> None:
        if self.active:
            self.bot.logger.warn("Tried starting signup task loop, but was already started")
            return
        self._start_dominion_loop()
        self._start_duo_loop()
        self._start_duel_loop()
        self.active = True
    
    async def stop(self) -> None:
        if not self.active:
            self.bot.logger.warn("Tried stopping signup task loop, but was already stopped")
            return
        
        self.dominion_task.stop()
        self.duo_task.stop()
        self.duel_task.stop()

        await self.dominion_message.delete()
        await self.duo_message.delete()
        await self.duel_message.delete()

        self.active = False
    
    def is_member_signed(self, member: Member) -> bool:
        return (
            member in self.dominion_signups 
            or member in self.duo_signups 
            or member in self.duel_signups
        )

    # Dominion loop

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
        
        self.dominion_task = Task(
            dominion_loop,
            IntervalTrigger(minutes=GAME_SIGNUP_INTERVAL)
        )
        self.dominion_task.start()

    async def _restart_dominion_loop(self):
        self.dominion_signups = [None for i in range(6)]
        self.num_dom_signups = 0
        await self.dominion_message.delete()

    # Duo loop

    def _start_duo_loop(self):

        #========================================================================
        async def duo_loop():
            if self.duo_message:
                await self._restart_duo_loop()
            
            signup_str: str = signup_list_to_string(self.duo_signups)
            embed = Embed(
                title="Duo PUG (2v2)",
                description=signup_str,
                footer=f"({self.num_duo_signups}/4)"
            )

            join_button = Button(
                style=ButtonStyle.GREEN,
                label="Join",
                custom_id="join_duo"
            )
            leave_button = Button(
                style=ButtonStyle.RED,
                label="Leave",
                custom_id="leave_duo"
            )
            button_row: list[ActionRow] = spread_to_rows(join_button, leave_button)

            self.duo_message = await self.channel.send(embed=embed, components=button_row)
        #========================================================================
        
        self.duo_task = Task(
            duo_loop,
            IntervalTrigger(minutes=GAME_SIGNUP_INTERVAL)
        )
        self.duo_task.start()

    async def _restart_duo_loop(self):
        self.duo_signups = [None for i in range(4)]
        self.num_duo_signups = 0
        await self.duo_message.delete()
    
    # Duel Loop

    def _start_duel_loop(self):

        #========================================================================
        async def duel_loop():
            if self.duel_message:
                await self._restart_duel_loop()
            
            signup_str: str = signup_list_to_string(self.duel_signups)
            embed = Embed(
                title="Duel PUG (1v1)",
                description=signup_str,
                footer=f"({self.num_duel_signups}/2)"
            )

            join_button = Button(
                style=ButtonStyle.GREEN,
                label="Join",
                custom_id="join_duel"
            )
            leave_button = Button(
                style=ButtonStyle.RED,
                label="Leave",
                custom_id="leave_duel"
            )
            button_row: list[ActionRow] = spread_to_rows(join_button, leave_button)

            self.duel_message = await self.channel.send(embed=embed, components=button_row)
        #========================================================================
        
        self.duel_task = Task(
            duel_loop,
            IntervalTrigger(minutes=GAME_SIGNUP_INTERVAL)
        )
        self.duel_task.start()

    async def _restart_duel_loop(self):
        self.duel_signups = [None for i in range(2)]
        self.num_duel_signups = 0
        await self.duel_message.delete()
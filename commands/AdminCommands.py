from interactions import (
    slash_command, slash_option, SlashContext, Extension, OptionType
)
from utils.const import COMMAND_PERMISSIONS

class AdminCommands(Extension):
    @slash_command(
        name="shutdown",
        description="Forcefully shutdown the bot",
        default_member_permissions=COMMAND_PERMISSIONS["ADMIN"]
    )
    @slash_option(
        name="log",
        description="Information for reason why bot was shutdown",
        opt_type=OptionType.STRING
    )
    async def shutdown_function(self, ctx: SlashContext, log: str=None):
        await ctx.send("Shutting down bot")
        if not log is None:
            self.bot.logger.info(f"Bot was forcefully shutdown for reason: {log}")
                
        self.bot.unload_extension("commands.BaseCommands")
        self.bot.unload_extension("commands.GameCommands")
        self.bot.unload_extension("commands.AdminCommands")
        self.bot.unload_extension("tasks.GameSignupManager")
        
        await self.bot.stop()

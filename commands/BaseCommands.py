from interactions import slash_command, SlashContext, Extension
from utils import utils


class BaseCommands(Extension):
    @slash_command(name="hello", description="Test command")
    async def test_function(self, ctx: SlashContext):
        await ctx.send("Hello World")
    
    @slash_command(name="test_error")
    async def test_error(self, ctx: SlashContext):
        await utils.error_embed(ctx, "test")
    
    @slash_command(name="test_success")
    async def test_success(self, ctx: SlashContext):
        await utils.success_embed(ctx, "test")
    
    @slash_command(name="test_response")
    async def test_response(self, ctx: SlashContext):
        await utils.general_embed(ctx, "test", "test")

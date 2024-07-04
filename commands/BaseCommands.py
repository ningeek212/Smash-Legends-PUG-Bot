from interactions import slash_command, SlashContext, Extension
from utils.utils import create_pages


class BaseCommands(Extension):
    @slash_command(name="hello", description="Test command")
    async def hello_function(self, ctx: SlashContext):
        await ctx.send("Hello World")
    
    @slash_command(name="test")
    async def test_function(self, ctx: SlashContext):
        info = [1, 2, 3, 4, 5, 6, 7]
        await create_pages(ctx, "Hello", info, elements_per_page=2)
from interactions import slash_command, SlashContext, Extension


class BaseCommandsTest(Extension):
    @slash_command(name="hello", description="Test command")
    async def test_function(self, ctx: SlashContext):
        await ctx.send("Hello World")

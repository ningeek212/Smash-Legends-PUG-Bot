from interactions import BaseContext, Embed, FlatUIColours, Color


async def error_embed(ctx: BaseContext, description: str):
    embed = Embed(title="Error ❌", description=description, color=FlatUIColours.POMEGRANATE)
    message = await ctx.send(embed=embed)
    return message


async def success_embed(ctx: BaseContext, description: str):
    embed = Embed(title="Success ✅", description=description, color=FlatUIColours.EMERLAND)
    message = await ctx.send(embed=embed)
    return message


async def general_embed(ctx: BaseContext, title: str, description: str, color: Color=FlatUIColours.AMETHYST):
    embed = Embed(title=title, description=description, color=color)
    message = await ctx.send(embed=embed)
    return message


async def create_pages(ctx: BaseContext):
    pass
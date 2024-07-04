from math import ceil
from interactions import Client, BaseContext, Embed, FlatUIColours, Color, ActionRow
from interactions import Button, ButtonStyle, component_callback, ComponentContext
from interactions.api.events import Component


async def error_embed(ctx: BaseContext, description: str):
    embed = Embed(title="Error ❌", description=description, color=FlatUIColours.POMEGRANATE)
    message = await ctx.send(embed=embed)
    return message


async def success_embed(ctx: BaseContext, description: str):
    embed = Embed(title="Success ✅", description=description, color=FlatUIColours.EMERLAND)
    message = await ctx.send(embed=embed)
    return message


async def general_embed(ctx: BaseContext, title: str, description: str,
                        color: Color=FlatUIColours.AMETHYST):
    embed = Embed(title=title, description=description, color=color)
    message = await ctx.send(embed=embed)
    return message


async def create_pages(
        ctx: BaseContext, title: str, info: list[str], if_empty: str="Empty List",
        sep: str="\n", elements_per_page: int=10):
    # If there are no elements, then return an empty page
    if not info:
        await ctx.send(embed=Embed(
            title=title,
            description=if_empty,
            color=FlatUIColours.POMEGRANATE
            ))
        return
    
    num_pages = ceil(len(info) / elements_per_page)
    pages = create_pages_str(info, sep, elements_per_page)
    current_page = 0
    
    page_buttons = ActionRow(
        Button(
            style=ButtonStyle.BLUE,
            label="Previous",
            custom_id="previous_page",
        ),
        Button(
            style=ButtonStyle.BLUE,
            label="Next",
            custom_id="next_page",
        ),
        Button(
            style=ButtonStyle.RED,
            label="Close",
            custom_id="close_page",
        )
    )

    embed = Embed(
        title=title,
        description=pages[current_page],
        color = FlatUIColours.AMETHYST
    )
    message = await ctx.send(embed=embed, components=page_buttons)

    while True:
        try:
            pressed_button: Component = await ctx.bot.wait_for_component(
                components=page_buttons, timeout=10
            )
        except TimeoutError:
            for button in page_buttons.components:
                button.disabled = True
            await message.edit(
                embed=Embed(
                    title=title,
                    description="Timed out",
                    color=FlatUIColours.AMETHYST
                ),
                components=page_buttons)
            return
        
        match pressed_button.ctx.custom_id:
            case "previous_page":
                current_page = (current_page - 1) % num_pages
                new_embed = Embed(
                    title=title,
                    description=pages[current_page],
                    color=FlatUIColours.AMETHYST
                )
                await pressed_button.ctx.edit_origin(embed=new_embed)
            case "next_page":
                current_page = (current_page + 1) % num_pages
                new_embed = Embed(
                    title=title,
                    description=pages[current_page],
                    color=FlatUIColours.AMETHYST
                )
                await pressed_button.ctx.edit_origin(embed=new_embed)
            case "close_page":
                for button in page_buttons.components:
                    button.disabled = True
                await pressed_button.ctx.edit_origin(
                    embed=Embed(
                        title=title,
                        description="Closed",
                        color=FlatUIColours.AMETHYST
                    ),
                    components=page_buttons)
                return


# Helper function to generate a list of strings of the pages
def create_pages_str(info: list, sep: str, elements_per_page: int):
    # Split the list of elements into lists with the appropiate number of elements
    pages = [info[a:(a+elements_per_page)] for a in range(0, len(info), elements_per_page)]
    # Convert the lists into strings
    return [sep.join(str(elem) for elem in l) for l in pages]

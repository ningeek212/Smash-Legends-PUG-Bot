from __future__ import annotations
from typing import TYPE_CHECKING
from math import ceil

from interactions import (
    BaseContext, Embed, FlatUIColours, Color, ActionRow, Member,
    Button, ButtonStyle, Message
)
from interactions.api.events import Component

if TYPE_CHECKING:
    from utils.types import Signups

async def error_embed(ctx: BaseContext, description: str) -> Message:
    embed = Embed(
        title="Error ❌",
        description=description,
        color=FlatUIColours.POMEGRANATE
    )
    message: Message = await ctx.send(embed=embed)
    return message


async def success_embed(ctx: BaseContext, description: str) -> Message:
    embed = Embed(
        title="Success ✅",
        description=description,
        color=FlatUIColours.EMERLAND
    )
    message: Message = await ctx.send(embed=embed)
    return message


async def general_embed(ctx: BaseContext, title: str, description: str,
                        color: Color=FlatUIColours.AMETHYST) -> Message:
    embed = Embed(
        title=title,
        description=description,
        color=color
    )
    message: Message = await ctx.send(embed=embed)
    return message


async def create_pages(
        ctx: BaseContext, title: str, info: list[str], page_title: str=None, if_empty: str="Empty List",
        sep: str="\n", elements_per_page: int=10) -> int:
    # If there are no elements, then return an empty page
    if not info:
        await ctx.send(embed=Embed(
            title=title,
            description=if_empty,
            color=FlatUIColours.POMEGRANATE
            ))
        return 0
    
    num_pages = ceil(len(info) / elements_per_page)
    if page_title:
        pages = create_pages_str(info, sep, elements_per_page, page_title)
    else:
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
        color = FlatUIColours.AMETHYST,
        footer=f"Page {current_page+1}/{num_pages}"
    )
    message: Message = await ctx.send(embed=embed, components=page_buttons)
    
    async def check(component: Component) -> bool:
        return component.ctx.message_id == message.id and component.ctx.author_id == ctx.author_id

    while True:
        try:
            pressed_button: Component = await ctx.bot.wait_for_component(
                components=page_buttons, check=check, timeout=30
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
            return 1
        
        match pressed_button.ctx.custom_id:
            case "previous_page":
                print(pressed_button.ctx.message_id)
                current_page = (current_page - 1) % num_pages
                new_embed = Embed(
                    title=title,
                    description=pages[current_page],
                    color=FlatUIColours.AMETHYST,
                    footer=f"Page {current_page+1}/{num_pages}"
                )
                await pressed_button.ctx.edit_origin(embed=new_embed)
            case "next_page":
                current_page = (current_page + 1) % num_pages
                new_embed = Embed(
                    title=title,
                    description=pages[current_page],
                    color=FlatUIColours.AMETHYST,
                    footer=f"Page {current_page+1}/{num_pages}"
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
                return 0


# Helper function to generate a list of strings of the pages
def create_pages_str(info: list, sep: str, elements_per_page: int, page_title: str=None) -> list[str]:
    # Split the list of elements into lists with the appropiate number of elements
    pages = [info[a:(a+elements_per_page)] for a in range(0, len(info), elements_per_page)]
    # Convert the lists into strings
    if page_title:
        pages = [page_title + sep + sep.join(str(elem) for elem in l) for l in pages]
    else:
        pages = [sep.join(str(elem) for elem in l) for l in pages]
    return pages

def signup_list_to_string(signups: Signups) -> str:
    signup_str: str = 'Signups:\n'
    for index, signup in enumerate(signups, 1):
        if signup is None:
            signup_str += f"{index}.\n"
        else:
            signup_str += f"{index}. <@{signup.id}>\n"
    return signup_str


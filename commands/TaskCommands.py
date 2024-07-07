from interactions import (
    Extension, slash_command, slash_option, SlashContext, OptionType, IntervalTrigger,
    Task, ChannelType, GuildText, Message, Embed, ActionRow, Button, ButtonStyle, 
    ComponentContext, component_callback
)
from utils.const import COMMAND_PERMISIONS
from utils.enums import TaskType
from utils.utils import general_embed, create_pages


class TaskCommands(Extension):
    pass

    # Tasks are organized by channel id, then task id, then 
    # tasks = {}
    
    # Dominion Loop creation command

    # @slash_command(
    #     name="start_dominion_loop",
    #     description="Starts the timed loop for dominion signups",
    #     default_member_permissions=COMMAND_PERMISIONS["TASK_LOOP"]
    # )
    # @slash_option(
    #     name="channel",
    #     opt_type=OptionType.CHANNEL,
    #     required=True,
    #     channel_types=[ChannelType.GUILD_TEXT],
    #     description="Which channel to start the loop in"
    # )
    # @slash_option(
    #     name="interval",
    #     opt_type=OptionType.INTEGER,
    #     required=False,
    #     description="How often should game signups be started/restarted (in minutes)",
    #     min_value=3
    # )
    # @slash_option(
    #     name="task_name",
    #     opt_type=OptionType.STRING,
    #     required=False,
    #     description="Name of the task you are starting"
    # )
    # async def dominion_loop_function(self, ctx: SlashContext, channel: GuildText, interval: int=5,
    #                                  task_name: str=None):
    #     task: Task = None
        
    #     async def dominion_loop():
    #         await channel.send("hi")
        
    #     task = Task(dominion_loop, IntervalTrigger(minutes=interval))
        
    #     button = Button(
    #         style=ButtonStyle.DANGER,
    #         label="Stop",
    #         custom_id="stop_task"
    #     )

    #     # Send initial message with button, then get/create the dictionary for the tasks within a
    #     # channel.  Put the task in said dictionary with its name, task object, and message object.
    #     # Edit the message to include the task name and channel id.
    #     message: Message = await ctx.send(content="Starting dominion task", components=button)
    #     channel_tasks: dict[str, tuple[Task, Message]] = self.tasks.setdefault(channel.id, {})
    #     if not task_name or task_name in self.tasks:
    #         task_name = f"Dominion Loop: {message.id}"
    #     await message.edit(content="Started dominion task", embed=Embed(
    #         description=f"{task_name}",
    #         footer=f"{channel.id}"
    #     ))

    #     channel_tasks[task_name] = (task, message)
    #     task.start()
    

    # # List channel tasks command

    # @slash_command(
    #     name="channel_tasks",
    #     description="Gets all the tasks for this specific channel",
    #     default_member_permissions=COMMAND_PERMISIONS["TASK_LOOP"]
    # )
    # @slash_option(
    #     name="channel",
    #     opt_type=OptionType.CHANNEL,
    #     required=False,
    #     description="The id of the channel you want the list of tasks for",
    #     channel_types=[ChannelType.GUILD_TEXT]
    # )
    # async def channel_tasks_function(self, ctx: SlashContext, channel: GuildText=None):
    #     if not channel:
    #         channel = ctx.channel
        
    #     channel_tasks: dict[str, tuple[Task, Message]] = self.tasks.get(channel.id)
    #     if not channel_tasks:
    #         await general_embed(ctx, "Tasks", "No tasks in this channel")
    #         return
        
    #     task_messages = [f"[{task_name}]({message[1].jump_url})" for (task_name, message) in channel_tasks.items()]
    #     await create_pages(ctx, "Tasks", task_messages)
    

    # # Stop Task button callback

    # @component_callback("stop_task")
    # async def stop_task_callback(self, ctx: ComponentContext):
    #     # Get the task information, and stop the task
    #     task_name: str = ctx.message.embeds[0].description
    #     task_channel = int(ctx.message.embeds[0].footer.text)
    #     task: tuple[Task, Message] = self.tasks[task_channel].pop(task_name)
    #     task[0].stop()

    #     # Disable the button and remove the embeds of the message
    #     await ctx.message.suppress_embeds()
    #     button = ctx.message.components[0].components[0]
    #     if isinstance(button, Button):
    #         button.disabled = True
    #     else:
    #         button = None

    #     await ctx.edit_origin(content="Stopped Task", components=button)


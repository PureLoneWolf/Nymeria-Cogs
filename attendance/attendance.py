import discord
from redbot.core import Config, commands
from redbot.core.bot import Red
import typing
from datetime import datetime


class Attendance(commands.Cog):
    def __init__(self, bot: Red):
        self.config = Config.get_conf(self, identifier=202005114)
        self.bot = bot
        default_guild = {
            "default_channel": None
        }
        self.config.register_guild(**default_guild)

# Commands

    @commands.command(name="attendance_channel", aliases=["attendchan"], help="Sets a default channel to post attendance command outputs.")
    @commands.has_permissions(administrator=True)
    async def _set_attendance_channel(self, ctx, channel: discord.TextChannel=None):
        if channel is None:
            await self.config.guild(ctx.guild).default_channel.set(None)
            await ctx.send("Attendance channel was reset, you will need to specify a channel to get attendance command outputs.")
        else:
            await self.config.guild(ctx.guild).default_channel.set(channel.id)
            await ctx.send(f"Attendance channel was set to {channel.mention}\nIf a channel is not specified in the attendance command I will output to {channel.mention}")

    @commands.command(name="attendance", aliases=["attend"], help="Lists all users in a voice channel and outputs them into a text channel.\n\nSubcommands:\n\nattend - outputs attendance \n\n**attendchan** - sets the default channel for output is no channel is specified")
    async def _attendance(self, ctx, voice: discord.VoiceChannel, role: typing.Optional[discord.Role]=None, channel: typing.Optional[discord.TextChannel]=None, per_page: int=20):
        channel_id = await self.config.guild(ctx.guild).default_channel()
        if not channel_id and not channel:
            await ctx.send("Specify a channel or set default channel.")
            return
        if not channel:
            channel = self.bot.get_channel(channel_id)
            if not channel:
                await ctx.send("Default channel is no longer valid please set a new one.")
                return
        e = discord.Embed(color=0x0000ff, timestamp=datetime.utcnow())
        if role:
            members = [m for m in voice.members if role in m.roles]
            text = f"Members with {role.mention} in channel **{voice.mention}**\n\n"
        else:
            text = ""
            members = [m for m in voice.members]
        members = sorted(members, key=lambda x: str(x.name).casefold())
        e.set_author(name=f"Attendance Info - ({len(members)})", icon_url=ctx.guild.icon_url)
        if len(members) == 0:
            await ctx.send("There's no one in this voice chat.")
            return
        page = 0
        if per_page == 0:
            texty = ""
            for m in members:
                if len(texty + f"{m}\n") > 2048:
                    e.description = text + texty
                    await channel.send(embed=e)
                    texty = ""
                texty += f"{m}\n"
            if texty != "":
                e.description = text + texty
                await channel.send(embed=e)
            return
        pages = self.paginate(members, per_page)
        e.description = text + pages[page]
        if len(pages) > 1:
            e.set_footer(text=f"Page {page+1} of {len(pages)}")
        sent = await channel.send(embed=e)
        if len(pages) == 1:
            return
        await sent.add_reaction("◀️")
        await sent.add_reaction("▶️")
        def check(reaction, user):
            return user == ctx.author and reaction.message.id == sent.id and str(reaction.emoji) in ["◀️", "▶️"]
        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=60)
                del user
            except:
                try:
                    await sent.clear_reactions()
                except:
                    break
                break
            if str(reaction.emoji) == "◀️":
                page -= 1
                if page < 0:
                    page = len(pages) - 1
            if str(reaction.emoji) == "▶️":
                page += 1
                if page > len(pages) - 1:
                    page = 0
            e.description = text + pages[page]
            e.set_footer(text=f"Page {page+1} of {len(pages)}")
            try:
                await sent.edit(embed=e)
            except:
                pass
            try:
                await reaction.remove(ctx.author)
            except:
                pass

    def paginate(self, members, per_page):
        pages = []
        text = ""
        i = 0
        for m in members:
            if i == per_page:
                i = 0
                pages.append(text)
                text = ""
            i += 1
            text += f"{m}\n"
        if text != "":
            pages.append(text)
        return pages

        



            
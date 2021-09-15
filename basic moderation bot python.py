from logging import error
import discord
from discord import channel
from discord import activity
from discord.ext import commands
import json

from discord.ext.commands.core import has_permissions

intents = discord.Intents.default()
intents.members - True

client = commands.Bot(command_prefix='!', intents=intents)


@client.event
async def on_ready():
    print("The bot is online.")
    print("------------------")
    await client.change_presence(status=discord.Status.idle, activity=discord.Streaming(name='chillin.', url='https://twitch.tv/ ENTER TWITCH URL'))


@client.command()
async def purge(ctx, amount=5):
    await ctx.channel.purge(limit=6)
    await ctx.send("Channel has recently been purged.", delete_after=1.0)


@client.command()
async def ping(ctx):
    await ctx.send(f'latency of me is {round(client.latency * 1000)}ms')


@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'user {member} has been kicked. F')


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the permission to kick.")


@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'user {member} has been banned.')


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the permission to ban.")


@client.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    embed = discord.Embed(
        title="muted", description=f"{member.mention} was muted ", colour=discord.Colour.light_gray())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" you have been muted from: {guild.name} reason: {reason}")


@client.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await member.send(f" you have unmutedd from: - {ctx.guild.name}")
    embed = discord.Embed(
        title="unmute", description=f" unmuted-{member.mention}", colour=discord.Colour.light_gray())
    await ctx.send(embed=embed)


client.run('ENTER BOT TOKEN HERE')

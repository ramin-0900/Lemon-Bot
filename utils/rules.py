import discord
from discord.ext import commands

class RoleManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='addrole', help='Adds a role to a specified user. Usage: !addrole @User RoleName')
    @commands.has_permissions(manage_roles=True)
    async def add_role(self, ctx, member: discord.Member, *, role: discord.Role):
        if role in member.roles:
            await ctx.send(f"User {member.mention} already has the `{role.name}` role.")
            return

        try:
            await member.add_roles(role)
            embed = discord.Embed(
                title="Role Added Successfully",
                description=f"Assigned the `{role.name}` role to {member.mention}.",
                color=discord.Color.green()
            )
            embed.set_footer(text=f"By: {ctx.author.name}", icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("I do not have permission to add this role. Please check my 'Manage Roles' permission.")
        except Exception as e:
            await ctx.send(f"An unexpected error occurred: {e}")

    @commands.command(name='removerole', help='Removes a role from a specified user. Usage: !removerole @User RoleName')
    @commands.has_permissions(manage_roles=True)
    async def remove_role(self, ctx, member: discord.Member, *, role: discord.Role):
        if role not in member.roles:
            await ctx.send(f"User {member.mention} does not have the `{role.name}` role.")
            return

        try:
            await member.remove_roles(role)
            embed = discord.Embed(
                title="Role Removed Successfully",
                description=f"Removed the `{role.name}` role from {member.mention}.",
                color=discord.Color.red()
            )
            embed.set_footer(text=f"By: {ctx.author.name}", icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("I do not have permission to remove this role.")
        except Exception as e:
            await ctx.send(f"An unexpected error occurred: {e}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the required permissions to use this command.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required arguments. Use `!help {ctx.command.name}` for more info.")
        elif isinstance(error, commands.RoleNotFound):
            await ctx.send(f"Role `{error.argument}` not found. Please check the role name.")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(f"Member `{error.argument}` not found. Please mention the user correctly.")

async def setup(bot):
    await bot.add_cog(RoleManager(bot))

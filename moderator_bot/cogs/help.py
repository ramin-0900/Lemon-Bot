import discord
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="Lemon-bot Help",
            description="",
            color=discord.Color.gold()
        )

        for cog_name in self.bot.cogs:
            cog = self.bot.get_cog(cog_name)
            cog_commands = cog.get_commands()
            if not cog_commands:
                continue

            command_list = [f"`!{c.name}` - {c.help or 'No description'}" for c in cog_commands]
            embed.add_field(
                name=cog_name,
                value="\n".join(command_list),
                inline=False
            )
        
        embed.set_footer(text="")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))

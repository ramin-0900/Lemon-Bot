import discord
from discord.ext import commands
import json
from pathlib import Path

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.descriptions = self._load_descriptions()

    def _load_descriptions(self):
        json_path = Path(__file__).parent.parent / "command_descriptions.json"
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {item['name']: item['description'] for item in data}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    @commands.command(name="help")
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="Lemon-bot Help",
            description="لیست تمام کامندهای موجود برای Lemon-bot:",
            color=discord.Color.gold()
        )

        for cog_name in self.bot.cogs:
            cog = self.bot.get_cog(cog_name)
            cog_commands = cog.get_commands()
            if not cog_commands:
                continue

            command_list = []
            for c in cog_commands:
                description = self.descriptions.get(c.name, "توضیحات موجود نیست.")
                command_list.append(f"`!{c.name}` - {description}")
            
            if command_list:
                embed.add_field(
                    name=cog_name,
                    value="\n".join(command_list),
                    inline=False
                )
        
        embed.set_footer(text="ساخته شده با 💛")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))

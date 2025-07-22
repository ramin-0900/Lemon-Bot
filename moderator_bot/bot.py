import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None,
    activity=discord.Game(name="!help"),
    status=discord.Status.online
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Discord.py API Version: {discord.__version__}")
    print("-------------------")
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"Loaded Cog: {filename}")
            except Exception as e:
                print(f"Failed to load cog {filename}: {e}")

# توکن ربات خود را در اینجا قرار دهید
# بهتر است این توکن را از یک فایل .env بخوانید
BOT_TOKEN = "YOUR_DISCORD_BOT_TOKEN"
bot.run(BOT_TOKEN)

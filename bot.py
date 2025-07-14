import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(dotenv_path='../.env')
TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    raise ValueError("DISCORD_TOKEN not found in .env file!")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print(f'Ready to serve in {len(bot.guilds)} guilds.')
    await bot.change_presence(activity=discord.Game(name="Managing Roles"))

@bot.event
async def setup_hook():
    print("Loading cogs...")
    try:
        await bot.load_extension('utils.rules')
        print("Successfully loaded RoleManager cog.")
    except Exception as e:
        print(f"Failed to load RoleManager cog: {e}")

if __name__ == "__main__":
    bot.run(TOKEN)

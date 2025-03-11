import discord
from discord.ext import commands
import re
import os
from myserver import server_on

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

suspicious_links = [
    r"steamcommunity\.com\/gift-card\/pay",
    r"steanmecomnmunity\.com\/\d+",
    r"freegift\.xyz",
    r"discordnitro\.xyz",
    r"nitrogift\.com",
    r"steamspecial\.xyz",
    r"freenitro\.club",
]

url_shorteners = [
    r"bit\.ly\/[a-zA-Z0-9]+",
    r"tinyurl\.com\/[a-zA-Z0-9]+",
    r"u\.to\/[a-zA-Z0-9]+",
    r"t\.co\/[a-zA-Z0-9]+",
    r"goo\.gl\/[a-zA-Z0-9]+",
]

EXEMPT_ROLE_ID = 1083402543989792839  # ID ของยศที่ได้รับการยกเว้น

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # ตรวจสอบว่าสมาชิกมียศที่ได้รับการยกเว้นหรือไม่
    if any(role.id == EXEMPT_ROLE_ID for role in message.author.roles):
        await bot.process_commands(message)
        return

    # ตรวจสอบข้อความว่ามีลิงก์ไวรัสหรือไม่
    for pattern in suspicious_links:
        if re.search(pattern, message.content, re.IGNORECASE):
            await message.delete()
            await message.channel.send(f"🚨 {message.author.mention} ห้ามโพสต์ลิงก์ต้องสงสัย! devby.น้อวโฟสสุดหล่อรวย")
            return

    # ตรวจสอบลิงก์ที่ถูกย่อ
    for shortener in url_shorteners:
        if re.search(shortener, message.content, re.IGNORECASE):
            await message.delete()
            await message.channel.send(f"🚨 {message.author.mention} ห้ามโพสต์ลิงก์ที่ถูกย่อ (อาจเป็นไวรัส)! devby.น้อวโฟสสุดหล่อรวย")
            return

    await bot.process_commands(message)

server_on()

bot.run(os.getenv('TOKEN'))

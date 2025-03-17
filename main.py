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

link_pattern = r"https?:\/\/\S+"

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

EXEMPT_ROLE_IDS = [1083402543989792839, 1297459096781455411, 1279035210855616513]
EXEMPT_CHANNEL_ID = 1338139756965396521
EXEMPT_CATEGORY_ID = 1279035381987151905  # เพิ่มหมวดหมู่ที่ละเว้น

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # ละเว้นข้อความในหมวดหมู่ที่ระบุ
    if message.channel.category and message.channel.category.id == EXEMPT_CATEGORY_ID:
        await bot.process_commands(message)
        return

    # ละเว้นช่องที่ระบุ
    if message.channel.id == EXEMPT_CHANNEL_ID:
        await bot.process_commands(message)
        return

    # ละเว้นสมาชิกที่มียศที่กำหนด
    if any(role.id in EXEMPT_ROLE_IDS for role in message.author.roles):
        await bot.process_commands(message)
        return

    if re.search(link_pattern, message.content, re.IGNORECASE):
        await message.delete()
        await message.channel.send(f"🚨 {message.author.mention} ห้ามโพสต์ลิงก์ในช่องนี้! devby.น้อวโฟสสุดหล่อรวย")
        return

    for pattern in suspicious_links:
        if re.search(pattern, message.content, re.IGNORECASE):
            await message.delete()
            await message.channel.send(f"🚨 {message.author.mention} ห้ามโพสต์ลิงก์ต้องสงสัย! devby.น้อวโฟสสุดหล่อรวย")
            return

    for shortener in url_shorteners:
        if re.search(shortener, message.content, re.IGNORECASE):
            await message.delete()
            await message.channel.send(f"🚨 {message.author.mention} ห้ามโพสต์ลิงก์ที่ถูกย่อ (อาจเป็นไวรัส)! devby.น้อวโฟสสุดหล่อรวย")
            return

    await bot.process_commands(message)

server_on()

bot.run(os.getenv('TOKEN'))

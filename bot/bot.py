import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from DB import DataBase

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
slash = SlashCommand(bot, override_type=True, sync_commands=True)
db = DataBase()
ids = []

@bot.event
async def on_ready():
    global ids
    await db.init()
    ids = [i.get("channel_id") for i in await db.get_ids()]

@bot.event
async def on_message(message):
    if message.channel.id in ids and not message.author.bot:
        for i in [b for b in ids if b != message.channel.id]:
            channel = bot.get_channel(i)
            webhook = await channel.create_webhook(name="Mazafacer")
            await webhook.send(content=message.content, username=message.author.name, avatar_url=message.author.avatar_url, wait=True)

@slash.slash(name="set")
async def set_channel(ctx: SlashContext, id_channel):
    global ids
    id_channel = int(id_channel)
    server = await db.search(ctx.guild_id)
    emb = discord.Embed(
        title="Канал успешно установлен!",
        description=f"""Канал <#{id_channel}> был успешно установлен.
        Теперь это канал в который будут приходить глобальные сообщения!""",
        color=0x00F2F9
    )

    if not id_channel in [i.id for i in ctx.guild.text_channels]:
        emb = discord.Embed(
            title="Ошибка!",
            description="Канала с таким id нет!",
            color=0xFF0000
        )
    
    elif server is None:
        await db.create(ctx.guild_id, id_channel)
        ids.append(id_channel)
    
    else:
        await db.update(ctx.guild_id, id_channel)
        ids = [i for i in ids if i != server.get("channel_id")] + [id_channel]
    

    return await ctx.send(embed=emb)
    

bot.run('token')

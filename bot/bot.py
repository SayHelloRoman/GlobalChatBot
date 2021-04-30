import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from DB import DataBase

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
bot.db = DataBase()
bot.ids = []
slash = SlashCommand(bot, override_type=True, sync_commands=True)

@bot.event
async def on_ready():
    await bot.db.init()
    bot.ids = [i.get("channel_id") for i in await bot.db.get_ids()]

@bot.event
async def on_message(message):
    if message.channel.id in bot.ids and not message.author.bot:
        for i in [b for b in bot.ids if b != message.channel.id]:
            channel = bot.get_channel(i)
            webhook = await channel.create_webhook(name="Mazafacer")
            await webhook.send(content=message.content, username=message.author.name, avatar_url=message.author.avatar_url, wait=True)
            await webhook.delete()

@slash.slash(name="set", guild_ids=[813735804030681199, 776525950681743410])
async def set_channel(ctx: SlashContext, id_channel):
    id_channel = int(id_channel)
    server = await bot.db.search(ctx.guild_id)
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
        await bot.db.create(ctx.guild_id, id_channel)
        bot.ids.append(id_channel)
    
    else:
        await bot.db.update(ctx.guild_id, id_channel)
        bot.ids = [i for i in bot.ids if i != server.get("channel_id")] + [id_channel]
    

    return await ctx.send(embed=emb)
    

bot.run('token')

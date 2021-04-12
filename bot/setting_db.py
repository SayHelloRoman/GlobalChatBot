import asyncio
import asyncpg
import json


async def setting():
    with open("config.json") as f:
        conn = await asyncpg.connect(
            **json.load(f)
        )

    await conn.execute('''
    CREATE TABLE guilds ( 
	id SERIAL PRIMARY KEY, 
	guild_id BIGINT, 
	channel_id BIGINT);
    ''')

    return await conn.close()


asyncio.run(setting())
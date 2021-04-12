from typing import Optional
import asyncio
import asyncpg
import json


def one_pool(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


@one_pool
class DataBase:
    async def init(self):
        with open("config.json") as f:
            self.conn = await asyncpg.connect(
                **json.load(f)
            )

    async def create(self, guild_id: Optional[int], channel_id: Optional[bool]):
        await self.conn.execute(
            f'''INSERT INTO guilds(guild_id, channel_id) VALUES({guild_id}, {channel_id})'''
        )
    
    async def update(self, guild_id: Optional[int], channel_id: Optional[bool]):
        await self.conn.execute(f"""
        UPDATE guilds SET 
        channel_id = {channel_id}
        WHERE guild_id = {guild_id}
        """)
    
    async def search(self, guild_id: Optional[int]):
        return await self.conn.fetchrow(f"SELECT * FROM guilds WHERE guild_id = {guild_id}")
    
    async def get_ids(self):
        return await self.conn.fetch(f"SELECT * FROM guilds")

# This file is a part of TG-FileStreamBot

import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from WebStreamer.vars import Var

class Database:
    def __init__(self, uri, database_name):
        self._client = AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.access_keys = self.db.access_keys

    def new_user(self, id):
        return dict(
            id=id,
            join_date=datetime.date.today().isoformat(),
            traffic_used=0,
            traffic_limit=0,  # 0 means no limit or default limit, handled in logic
            is_premium=False
        )

    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    async def get_user(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user

    async def update_user_usage(self, id, used_bytes):
        await self.col.update_one(
            {'id': int(id)},
            {'$inc': {'traffic_used': used_bytes}}
        )

    async def add_premium(self, id, limit_bytes):
        await self.col.update_one(
            {'id': int(id)},
            {'$set': {'traffic_limit': limit_bytes, 'is_premium': True}}
        )

    async def remove_premium(self, id):
        await self.col.update_one(
            {'id': int(id)},
            {'$set': {'traffic_limit': 0, 'is_premium': False}}
        )

    async def create_access_key(self, key, description=""):
        await self.access_keys.insert_one({'key': key, 'description': description, 'used_by': []})

    async def get_access_key(self, key):
        return await self.access_keys.find_one({'key': key})

    async def use_access_key(self, key, user_id):
        await self.access_keys.update_one(
            {'key': key},
            {'$push': {'used_by': user_id}}
        )

db = Database(Var.DATABASE_URL, "TG-FileStreamBot")

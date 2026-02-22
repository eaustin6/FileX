import datetime
import motor.motor_asyncio
from WebStreamer.vars import Var

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.pk = self.db.pass_keys

    def new_user(self, id):
        return dict(
            _id=int(id),
            quota=Var.DEFAULT_QUOTA,  # Default quota in bytes
            used=0,
            join_date=datetime.datetime.now()
        )

    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        return self.col.find({})

    async def delete_user(self, user_id):
        await self.col.delete_many({'_id': int(user_id)})

    async def get_user(self, id):
        return await self.col.find_one({'_id': int(id)})

    async def update_user_quota(self, id, amount):
        # amount can be positive (grant) or negative (revoke)
        await self.col.update_one({'_id': int(id)}, {'$inc': {'quota': amount}})

    async def update_user_used(self, id, amount):
        await self.col.update_one({'_id': int(id)}, {'$inc': {'used': amount}})

    async def reset_user_used(self, id):
        await self.col.update_one({'_id': int(id)}, {'$set': {'used': 0}})

    async def create_pass_key(self, key, type, value=0):
        # type: "access" or "premium"
        # value: quota amount for premium
        await self.pk.insert_one({
            '_id': key,
            'type': type,
            'value': value,
            'created_at': datetime.datetime.now()
        })

    async def get_pass_key(self, key):
        return await self.pk.find_one({'_id': key})

    async def delete_pass_key(self, key):
        await self.pk.delete_one({'_id': key})

db = Database(Var.DATABASE_URL, Var.SESSION_NAME)

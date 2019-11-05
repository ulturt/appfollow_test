from motor.motor_asyncio import AsyncIOMotorClient

from settings import MONGO_HOST, MONGO_PORT, MONGO_DATABASE


def init_mongo():
    mongo_uri = f'mongodb://{MONGO_HOST}:{MONGO_PORT}'
    client = AsyncIOMotorClient(mongo_uri)
    db = client[MONGO_DATABASE]
    return db

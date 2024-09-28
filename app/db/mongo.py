from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

mongo_client = None

async def connect_to_mongo():
    global mongo_client
    mongo_client = AsyncIOMotorClient(settings.MONGO_URI)
    print(f"Conectado a MongoDB: {settings.MONGO_URI}")

async def close_mongo_connection():
    global mongo_client
    if mongo_client:
        mongo_client.close()
        print("Conexión a MongoDB cerrada")

def get_mongo_client():
    global mongo_client
    if mongo_client is None:
        raise Exception("MongoClient no inicializado. Asegúrate de llamar a connect_to_mongo() primero.")
    return mongo_client

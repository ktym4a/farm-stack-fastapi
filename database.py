from decouple import config
import motor.motor_asyncio

MONGO_API_KEY = config("MONGO_API_KEY")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_API_KEY)
database = client.API_DB
collenction_todo = database.todo
collenction_user = database.user

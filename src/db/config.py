import os

from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

class ConfigDB:
    def __init__(self):
        self.MONGO_DB_URI = os.getenv("MONGO_DB_URI")

    def connectDB(self):
        client = MongoClient(self.MONGO_DB_URI, server_api = ServerApi('1'))
        try:
            client.admin.command('ping')
            print("MongoDB client successfully connected")
            return client
        except Exception as e:
            print(f"Error while connecting MongoDB client : {e}")

    def disconnectDB(self, client : MongoClient):
        try:
            client.close()
            print("MongoDB client successfully disconnected")
        except Exception as e:
            print(f"Error while disconnecting MongoDB client : {e}")

    def createDB(self):
        try:
            client = self.connectDB()
            db = client.Auth
            user_db = db["user"]
            return user_db
        except Exception as e:
            print(f"Error while creating collection : {e}")
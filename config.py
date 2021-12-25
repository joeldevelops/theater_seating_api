import os

MONGODB_DB = os.environ.get("MONGO_NAME")
MONGODB_HOST = os.environ.get("MONGO_HOST", "localhost")
MONGODB_PORT = int(os.environ.get("MONGO_PORT", 27017))
MONGODB_CONNECT = True if os.environ.get("MONGO_CONNECT_ON_STARTUP", False) == "True" else False
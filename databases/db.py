from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Get the MongoDB URI from environment variable
uri = os.getenv("ATLAS_URI")

if not uri:
    raise RuntimeError("❌ No se encontró la variable ATLAS_URI en el archivo .env")

# Connect to MongoDB using Stable API version 1
client = MongoClient(uri, server_api=ServerApi("1"))

# Use the EvolveCRM database
db = client["EvolveCRM"]

# Collections used in your CRM
usuarios_collection = db["usuarios"]
facturas_collection = db["facturas"]
log_collection = db["log"]

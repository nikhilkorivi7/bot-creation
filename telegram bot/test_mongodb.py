from pymongo import MongoClient

MONGODB_URI = "mongodb+srv://<admin>:<root>@<first>.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGODB_URI)

try:
    client.admin.command('ping')
    print("✅ MongoDB Connection Successful!")
except Exception as e:
    print(f"❌ MongoDB Connection Failed: {e}")

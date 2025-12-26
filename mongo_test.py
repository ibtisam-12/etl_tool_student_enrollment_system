from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["enrollment_db"]
print("Mongo OK. Collections:", db.list_collection_names())

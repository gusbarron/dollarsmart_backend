import pymongo
import certifi

con_str = "mongodb+srv://gusbarron:LACIEgus11!!@cluster0.lbhklne.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_str, tlsCAFile=certifi.where())

db = client.get_database("Candystore")


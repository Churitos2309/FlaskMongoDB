from pymongo import MongoClient
import certifi


MONGO_URI = 'mongodb+srv://JuanOchoa:ANA2000JUAN@cluster0.cof4rpm.mongodb.net/'

ca = certifi.where()

def dbConnection():
    try:
        client = MongoClient(MONGO_URI, tlsCaFile=ca)
        db = client["dbb_productos_app"]
        
    except ConnectionError:
        print("No se ha podido conectar con la base de datos")
    
    return db


def fileStorePath():
    return "/home/sergey/soundexfiles/"

def mongoDatabaseName():
    return "test_database"

def mongoConnect():
    from pymongo import MongoClient
    return MongoClient()
    

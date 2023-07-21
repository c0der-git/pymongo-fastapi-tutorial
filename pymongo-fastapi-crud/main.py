import os
from fastapi import FastAPI
#from dotenv import dotenv_values
from dotenv import load_dotenv
from pymongo import MongoClient
from routes import router as book_router

#config = dotenv_values(".env")
load_dotenv()

mongo_user = os.getenv('MONGO_USERNAME')
mongo_pass = os.getenv('MONGO_PASSWORD')
mongo_dbname = os.getenv('MONGO_DATABASE')
mongo_addr = os.getenv('MONGO_URI')
mongo_port = int(os.getenv('MONGO_PORT'))


app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    print("MONGO_URI: " + os.getenv('MONGO_URI'))
    print("MONGO_DATABASE: " + os.getenv('MONGO_DATABASE'))
    #   print("MONGO_URI: " + config["MONGO_URI"])
    #   print("MONGO_DATABASE: " + config["MONGO_DATABASE"])

    app.mongodb_client = MongoClient(mongo_addr, mongo_port, username=mongo_user, password=mongo_pass)
    app.database = app.mongodb_client[mongo_dbname]
    #app.mongodb_client = MongoClient(os.getenv('MONGO_URI'),)
    #app.database = app.mongodb_client[os.getenv('MONGO_DATABASE')]
    #app.mongodb_client = MongoClient(config["MONGO_URI"])
    #app.database = app.mongodb_client[config["MONGO_DATABASE"]]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(book_router, tags=["books"], prefix="/book")
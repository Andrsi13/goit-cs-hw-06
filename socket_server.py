import socket
import pymongo
from datetime import datetime
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://username:password@cluster.mongodb.net/test")
MONGO_DB = os.getenv("MONGO_DB", "message_db")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "messages")

client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

def run_socket_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(('0.0.0.0', 5000))
        while True:
            data, _ = sock.recvfrom(1024)
            message = eval(data.decode())
            message["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            collection.insert_one(message)

if __name__ == '__main__':
    run_socket_server()

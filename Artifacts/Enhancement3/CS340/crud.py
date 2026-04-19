from __future__ import annotations

from pymongo import MongoClient
from pymongo.errors import PyMongoError



class AnimalShelter:
    #CRUD operations for the animals collection in MongoDB.

    def __init__(
        self,
        host: str = "localhost",
        port: int = 27017,
        db: str = "AAC",
        collection: str = "animals",
        user: str | None = None,
        password: str | None = None,
    ) -> None:
        #Create a database connection and select the target collection.
        if user and password:
            connection_uri = f"mongodb://{user}:{password}@{host}:{port}"
        else:
            connection_uri = f"mongodb://{host}:{port}"

        try:
            self.client = MongoClient(connection_uri, serverSelectionTimeoutMS=5000)
            self.client.admin.command("ping")
            self.database = self.client[db]
            self.collection = self.database[collection]
        except PyMongoError as exc:
            raise ConnectionError(f"Failed to connect to MongoDB: {exc}") from exc

    def create(self, data: dict) -> bool:
        #Insert one document into the collection.
        if not isinstance(data, dict) or not data:
            raise ValueError("Data must be a non-empty dictionary")

        try:
            result = self.collection.insert_one(data)
            return result.acknowledged
        except PyMongoError:
            return False

    def read(self, query: dict | None = None) -> list[dict]:
        #Return all documents matching a MongoDB query.
        if query is None:
            query = {}
        if not isinstance(query, dict):
            raise ValueError("Query must be a dictionary")

        try:
            results = self.collection.find(query)
            return list(results)
        except PyMongoError:
            return []
        
    def aggregate(self, pipeline: list[dict]) -> list[dict]:
    #Run an aggregation pipeline against the collection.
        try:
            results = self.collection.aggregate(pipeline)
            return list(results)
        except PyMongoError:
            return []

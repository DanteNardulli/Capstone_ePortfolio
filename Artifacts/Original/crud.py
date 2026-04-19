from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter:
    """CRUD operations for the 'animals' collection in MongoDB"""

    def __init__(self, user="aacuser", password="SNHU1234", host="nv-desktop-services.apporto.com", port=31580, db="AAC", collection="animals"):
        try:
            self.client = MongoClient(f'mongodb://{user}:{password}@{host}:{port}')
            self.database = self.client[db]
            self.collection = self.database[collection]
        except Exception as e:
            raise Exception(f"Failed to connect to MongoDB: {e}")

    def create(self, data):
        """Inserts a document into the database."""
        if data and isinstance(data, dict):
            try:
                result = self.collection.insert_one(data)
                return result.acknowledged  # Returns True if the insertion was successful
            except Exception as e:
                print(f"Error inserting document: {e}")
                return False
        else:
            raise ValueError("Data must be a non-empty dictionary")

    def read(self, query=None):
        """Retrieves documents based on the given query."""
        if query is None:
            query = {}

        if isinstance(query, dict):
            try:
                results = self.collection.find(query)
                return list(results)
            except Exception as e:
                print(f"Error retrieving documents: {e}")
                return []
        else:
            raise ValueError("Query must be a dictionary")
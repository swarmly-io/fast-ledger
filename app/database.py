import couchdb
import json
from decimal import Decimal
from uuid import UUID
from datetime import datetime, date  
from fastapi.logger import logger

class JSONEncoderExtended(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, UUID):
            return str(obj)
        elif isinstance(obj, Decimal):
            return str(obj)

        return json.JSONEncoder.default(self, obj)

class Database:
    def __init__(self):
        self.couch = self.get_client()
        couchdb.json.use(decode=Database.decode_json, encode=Database.encode_json)
        self.update_db_list()
        logger.warn(self.dbs)
        
    def update_db_list(self):
        status, _, self.dbs = self.couch.resource.get_json('_all_dbs')
        if (status != 200):
            raise Exception("Couldn't connect to db")
        
    def get_client(self):
        return couchdb.Server('http://admin:password@localhost:5984/')

    @staticmethod
    def encode_json(obj):
        return json.dumps(obj, cls=JSONEncoderExtended)
    @staticmethod
    def decode_json(obj):
        return json.loads(obj)

    @staticmethod
    def todict(obj, classkey=None):
        if isinstance(obj, dict):
            data = {}
            for (k, v) in obj.items():
                data[k] = Database.todict(v, classkey)
            return data
        elif hasattr(obj, "_ast"):
            return Database.todict(obj._ast())
        elif isinstance(obj, list) and not isinstance(obj, str):
            return [Database.todict(v, classkey) for v in obj]
        elif hasattr(obj, "__dict__"):
            data = dict([(key, Database.todict(value, classkey)) 
                for key, value in obj.__dict__.items() 
                if not callable(value) and not key.startswith('_')])
            if classkey is not None and hasattr(obj, "__class__"):
                data[classkey] = obj.__class__.__name__
            return data
        else:
            return obj
from enum import Enum
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
    
class Buckets(str,Enum):
    BANK = "bank"
    ENTITIES = "entities"
    ASSETS = "assets"
    LIABILITIES = "liabilities"
    TRANSACTIONS = "transactions"
    VALUATIONS = "valuations"
    LOCATIONS = "locations"

class DocumentDatabase:
    def __init__(self):
        self.couch = self.get_client()
        couchdb.json.use(decode=DocumentDatabase.decode_json, encode=DocumentDatabase.encode_json)
        self.update_db_list()
        logger.warn(self.dbs)
        
    def update_db_list(self):
        status, _, self.dbs = self.couch.resource.get_json('_all_dbs')
        if (status != 200):
            raise Exception("Couldn't connect to db")
        
    def get_client(self):
        return couchdb.Server('http://admin:password@localhost:5984/')
    
    def get_last_id(self, bucket_name):
        x = self.couch[bucket_name].changes(include_docs=True, descending=True, limit=1)
        if not x['results'] or len(x['results']) == 0:
            return None
        return x['results'][0]['id']

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
                data[k] = DocumentDatabase.todict(v, classkey)
            return data
        elif hasattr(obj, "_ast"):
            return DocumentDatabase.todict(obj._ast())
        elif isinstance(obj, list) and not isinstance(obj, str):
            return [DocumentDatabase.todict(v, classkey) for v in obj]
        elif hasattr(obj, "__dict__"):
            data = dict([(key, DocumentDatabase.todict(value, classkey)) 
                for key, value in obj.__dict__.items() 
                if not callable(value) and not key.startswith('_')])
            if classkey is not None and hasattr(obj, "__class__"):
                data[classkey] = obj.__class__.__name__
            return data
        else:
            return obj
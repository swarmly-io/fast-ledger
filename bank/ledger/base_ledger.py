from uuid import UUID
from pydantic import BaseModel
from bank.persistence.database import Buckets, DocumentDatabase
from bank.persistence.transactional_database import TransactionalDatabase

class IdDto(BaseModel):
    id: UUID

class BaseLedger:
    def __init__(self, documents: DocumentDatabase, transactional: TransactionalDatabase, logger):
        self.documents = documents
        self.transactional = transactional
        self.logger = logger
        
    def get_db(self, bucket : str = Buckets.BANK.value):
        couch = self.documents.couch
        if bucket not in self.documents.dbs:
            couch.create(bucket)
            self.documents.update_db_list()
        db = couch[bucket]
        return db
    
from bank.persistence.database import Database
from bank.persistence.transactional_database import TransactionalDatabase


class BaseLedger:
    def __init__(self, documents: Database, transactional: TransactionalDatabase, logger):
        self.documents = documents
        self.transactional = transactional
        self.logger = logger
        
    def get_db(self, bucket : str = 'bank'):
        couch = self.documents.couch
        if bucket not in self.documents.dbs:
            couch.create(bucket)
            self.documents.update_db_list()
        db = couch[bucket]
        return db
class BaseLedger:
    def __init__(self, documents, transactional, logger):
        self.documents = documents
        self.transactional = transactional
        self.logger = logger
        
    def get_db(self, bucket : str = 'bank'):
        couch = self.documents.couch
        db = couch[bucket] if bucket in self.documents.dbs else couch.create(bucket)
        return db
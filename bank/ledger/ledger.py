from bank.ledger.assets_ledger import AssetsLedger
from bank.ledger.bank_ledger import BankLedger
from bank.ledger.entities_ledger import EntitiesLedger
from bank.ledger.transaction_ledger import TransactionsLedger
from bank.persistence.database import DocumentDatabase
from bank.persistence.transactional_database import TransactionalDatabase

class Ledger(EntitiesLedger, TransactionsLedger, BankLedger, AssetsLedger):
    def __init__(self, documents: DocumentDatabase, transactional: TransactionalDatabase, logger):
        super().__init__(documents, transactional, logger)
    
    
from bank.ledger.entities_ledger import EntitiesLedger
from bank.ledger.bank_ledger import BankLedger
from bank.ledger.transaction_ledger import TransactionsLedger

class Ledger(EntitiesLedger, TransactionsLedger):
    def __init__(self, documents, transactional, logger):
        super().__init__(documents, transactional, logger)
    
    



from typing import List, Union
from fastapi import APIRouter, Query
from bank.ledger import TransactionsLedger

from bank.ledger_models import EntityEntry, TransactionEntry
from routes import documents, transactional, logger

router = APIRouter(prefix='/api')
@router.startup()
def startup():
    router.ledger = TransactionsLedger(documents, transactional, logger)
    
@router.get("/transactions", response_model=List[TransactionEntry])
def get_transactions(offset: int = 0, limit: int = Query(default=100, lte=100)):
    return router.ledger.get_transactions(offset, limit)
        
class TransactionDto:
    transactionEntry: TransactionEntry
    entity: EntityEntry
    
@router.post("/transaction")
def create_transaction(transaction: Union[TransactionDto, TransactionEntry]):
    if isinstance(transaction, TransactionDto):
        return router.ledger.create_transaction(transaction.transactionEntry, transaction.entity)
    else:
        return router.ledger.create_transaction(transaction)

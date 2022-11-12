


from typing import List, Union
from fastapi import APIRouter, Query
from bank.bank_models import Transaction
from bank.ledger.ledger import TransactionsLedger
from bank.ledger.transaction_ledger import TransactionDto

from . import documents, transactional, logger

router = APIRouter(prefix='/api')
@router.on_event("startup")
def startup():
    router.ledger = TransactionsLedger(documents, transactional, logger)
    
@router.get("/transactions", response_model=List[Transaction])
def get_transactions(offset: int = 0, limit: int = Query(default=100, lte=100)):
    return router.ledger.get_transactions(offset, limit)
    
@router.post("/transaction")
def create_transaction(transaction: Union[TransactionDto, Transaction]):
        return router.ledger.create_transaction_from_dto(transaction)

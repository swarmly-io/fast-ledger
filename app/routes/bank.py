

from fastapi import APIRouter
from bank.ledger.ledger import BankLedger
from . import documents, transactional, logger

router = APIRouter(prefix='/api', tags=["bank"])

@router.on_event("startup")
def startup():
    router.ledger = BankLedger(documents, transactional, logger)    

@router.post("/runledger")
def compute_balances():
    return router.ledger.compute_balances()







 
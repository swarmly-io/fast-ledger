

from fastapi import APIRouter
from bank.ledger import BankLedger
from . import documents, transactional, logger

router = APIRouter(prefix='/api')

@router.on_event("startup")
def startup():
    router.ledger = BankLedger(documents, transactional, logger)    

@router.post("/runledger")
def compute_balances():
    return router.ledger.compute_balances()







 
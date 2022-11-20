
from fastapi import APIRouter

from bank.entities_models import AccountEntity
from bank.ledger.entities_ledger import AccountEntityEditDto, IdDto, CreateAccountDto, EntitiesLedger
from . import documents, transactional, logger

router = APIRouter(prefix='/api')

@router.on_event("startup")
def startup():
    router.ledger = EntitiesLedger(documents, transactional, logger)

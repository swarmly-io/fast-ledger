
from fastapi import APIRouter

from bank.entity_models import AccountEntity
from bank.ledger import EntitiesLedger
from . import documents, transactional, logger

router = APIRouter(prefix='/api')

@router.on_event("startup")
def startup():
    router.ledger = EntitiesLedger(documents, transactional, logger)

@router.get("/entities")
def get_entities():
    return router.ledger.get_entities()

@router.post("/account_entity")
def create_account_entity(entity: AccountEntity):
    return router.ledger.get_account_entity(entity)
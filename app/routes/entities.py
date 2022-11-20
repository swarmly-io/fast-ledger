
from fastapi import APIRouter

from bank.entities_models import AccountEntity
from bank.ledger.base_ledger import IdDto
from bank.ledger.entities_ledger import AccountEntityEditDto, CreateAccountDto, EntitiesLedger
from . import documents, transactional, logger

router = APIRouter(prefix='/api', tags=["accounts"])

@router.on_event("startup")
def startup():
    router.ledger = EntitiesLedger(documents, transactional, logger)

@router.get("/entities")
def get_entities():
    return router.ledger.get_entities()

@router.post("/entities/init")
def create_account_entity(entity: AccountEntity):
    try:
        return router.ledger.create_account_entity(entity)
    except Exception as e:
        logger.error(e)
        raise e

@router.post("/account/close")
def close_account_entity(closeDto: IdDto):
    return router.ledger.close_entity(closeDto)
    
@router.post("/account/entity/edit")
def edit_account_entity(entityDto: AccountEntityEditDto):
    return router.ledger.edit_account(entityDto)

@router.post("/account/create")
def create_account(account_details: CreateAccountDto):
    return router.ledger.add_account(account_details.account_id, account_details.account)

@router.post("/account/get_latest_balances")
def get_latest_balances(idDto: IdDto):
    return router.ledger.get_balances(idDto)
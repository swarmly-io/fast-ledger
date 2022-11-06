


from typing import List
from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.transactional_database import TransactionalDatabase
from bank.entity_models import Transaction
from bank.ledger import EntityEntry, TransactionEntry
from sqlmodel import select

router = APIRouter(prefix='/api')

@router.on_event("startup")
def startup_event():
    router.db = TransactionalDatabase()
    
class TransactionDto(BaseModel):
    from_entity: EntityEntry 
    to_entity: EntityEntry 
    transaction: TransactionEntry
    
@router.get("/transactions", response_model=List[TransactionEntry])
def get_transactions(offset: int = 0, limit: int = Query(default=100, lte=100)):
    with router.db.get_session() as session:
        transactions = session.exec(select(TransactionEntry).offset(offset).limit(limit)).all()
        return transactions
        
def entity_exists(session, id):
    entity = session.exec(select(EntityEntry).where(EntityEntry.id == id)).one()
    return True if entity else False
        

@router.post("/transaction")
def create_transaction(transaction: TransactionDto):
    with router.db.get_session() as session:
        if not entity_exists(session, transaction.from_entity.id): 
            session.add(transaction.from_entity)
        if not entity_exists(session, transaction.to_entity.id):
            session.add(transaction.to_entity)

        transaction.transaction.from_id = transaction.from_entity.id
        transaction.transaction.to_id = transaction.to_entity.id
        session.add(transaction.transaction)
        session.commit()
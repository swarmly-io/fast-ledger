from typing import Union
from fastapi import Query
from pydantic import BaseModel
from sqlmodel import select
from bank.bank_models import Entity, Transaction
from bank.ledger.base_ledger import BaseLedger

from bank.ledger.ledger_models import EntityEntry, TransactionEntry

class TransactionDto(BaseModel):
    counter_party: Entity
    transaction: Transaction

class TransactionsLedger(BaseLedger):
    def get_transactions(self, offset: int = 0, limit: int = Query(default=100, lte=100)):
        with self.documents.get_session() as session:
            transactions = session.exec(select(TransactionEntry).offset(offset).limit(limit)).all()
            return transactions
        
    def entity_exists(self, session, id):
        entity = session.exec(select(EntityEntry).where(EntityEntry.entity_id == id)).one_or_none()
        return True if entity else False
    
    def create_transaction_from_dto(self, transactiondto: Union[TransactionDto,Transaction]):
        if isinstance(transactiondto, TransactionDto):
            entityEntry = EntityEntry(**transactiondto.counter_party.__dict__)
            transaction = TransactionEntry(**transactiondto.transaction)
            return self.create_transaction(transaction, entityEntry)
        else:
            transaction = TransactionEntry(**transactiondto.transaction)
            return self.create_transaction(transaction)
    
    def create_transaction(self, transaction: TransactionEntry, entity: EntityEntry = None):
        with self.transactional.get_session() as session:
            if entity:
                if not self.entity_exists(session, entity.entity_id): 
                    session.add(entity)
                transaction.counter_party_entity_id = entity.entity_id
                session.add(transaction)
                session.commit()
            else:
                if not self.entity_exists(session, transaction.counter_party_entity_id): 
                    raise Exception("No valid counterparty provided")
                session.add(transaction)
                session.commit()
from copy import deepcopy
import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel
from bank.ledger.bank_ledger import BankLedger
from bank.persistence.database import Database
from bank.entity_models import Account, AccountEntity, Address, IdDocument, PhoneNumber
from sqlmodel import select

from bank.ledger.ledger_models import AccountEntry, EntityEntry

class CreateAccountDto(BaseModel):
    account_id: UUID
    account: Account

class EntityIdDto(BaseModel):
    id: UUID

class AccountEntityEditDto(BaseModel):
    entity_id: UUID
    first_name: Optional[str] 
    middle_name: Optional[str]
    last_name: Optional[str]
    id_documents: Optional[List[IdDocument]]
    place_of_birth: Optional[str]
    addresses: Optional[List[Address]]
    phone_numbers: Optional[List[PhoneNumber]]
    
class BalanceDto(BaseModel):
    balance: Decimal
    balance_currency: str
    date_updated: datetime.datetime

class EntitiesLedger(BankLedger):
    def get_entity_by_id(self, id: UUID, bucket: str = "bank"):
        db = self.get_db(bucket)
        return db.get(str(id))
    
    def get_entities(self, bucket: str = "bank"):
        db = self.get_db(bucket)
        docs = db.get("_all_docs")['rows']
        self.logger.warn(docs)
        entities = [db.get(d['id']) for d in docs]
        return entities
    
    def create_account_entity(self, entity: AccountEntity, bucket: str = "bank"):
        db = self.get_db(bucket)
        
        dbentity = Database.todict(entity)
        dbentity["_id"] = str(entity.id)
        existing = db.get(str(dbentity["_id"]))
        self.logger.warn(existing)
        if existing:
            self.logger.warn("Updating")
            dbentity['_rev'] = existing['_rev']
            db.save(dbentity)
        else:
            self.logger.warn("Creating")
            db.save(dbentity)

            with self.transactional.get_session() as session:
                entity_entry = EntityEntry(first_name=entity.first_name, last_name=entity.last_name, entity_id=entity.id)
                session.add(entity_entry)
                session.commit()
                
            for account in entity.accounts:
                self.create_account_entry(AccountEntry(entity_id=entity.id, account_id=account.id, currency=account.balanceCurrency))

        return entity 
    
    def add_account(self, entity_account_id: UUID, account: Account, bucket: str = "bank"):
        with self.transactional.get_session() as session:
            db = self.get_db(bucket)
            entity: AccountEntity = db.get(str(entity_account_id))
            if not entity:
                raise Exception("No entity exists to create new account")

            
            entity_entry = session.exec(select(EntityEntry).where(EntityEntry.account_id == id)).one_or_none()
            if not entity_entry:
                raise Exception("No entity entry exists for account")

            # create ledger entry
            account_id = uuid4()
            account_entry = AccountEntry(entity_id=entity_account_id, account_id=account_id)
            session.add(account_entry)
            session.commit()
            
            # create document entry
            account.id = account_id
            entity.accounts.append(account)
            db.save(entity)
            
    def edit_entity(self, edit: AccountEntityEditDto, bucket: str = "bank"):
        entity = self.get_entity_by_id(edit.entity_id, bucket)
        if not entity:
            raise Exception("Entity not found")

        entitydict = deepcopy(entity).update(edit.__dict__)
        newentity = AccountEntity(**entitydict)
        db = self.get_db(bucket)
        db.save(newentity)
            
    def close_entity(self, close: EntityIdDto, bucket: str = "bank"):
        entity: AccountEntity = self.get_entity_by_id(close.entity_id, bucket)
        if not entity:
            raise Exception("Entity not found")
        
        with self.transactional.get_session() as session:
            for account in entity.accounts:
                account.closed_date = datetime.datetime.utcnow()
                account_entry: AccountEntry = session.exec(select(AccountEntry).where(AccountEntry.account_id == account.id and AccountEntry.entity_id == entity.id)).one_or_none()
                if not account_entry:
                    raise Exception("Couldn't find account entry")
                account_entry.closed_date = datetime.datetime.utcnow()
                account_entry.add(account_entry)
                session.commit()
            
        entity.closed_date = datetime.datetime.utcnow()
        db = self.get_db(bucket)
        db.save(entity)
        
    def get_balances(self, idDto: EntityIdDto):
        account_balances = {}
        with self.transactional.get_session() as session:
            accounts = session.exec(select(AccountEntry).where(AccountEntry.entity_id == idDto.id)).all()
            for a in accounts:
                account_balances[a.account_id] = {}
                if a.balances:
                    for b in a.balances:
                        account_balances[a.account_id][b.currency] = BalanceDto(balance=b.balance, balance_currency=b.currency, date_updated=b.date_updated)
        return account_balances
        
import datetime
from decimal import Decimal
from typing import Optional, Union
from uuid import UUID
from fastapi import Query
from pydantic import BaseModel
from bank.persistence.database import Database
from bank.entity_models import AccountEntity
from sqlmodel import select

from bank.ledger_models import AccountEntry, BalanceEntry, EntityEntry, TransactionEntry

class TransactionDto(BaseModel):
    counter_party: EntityEntry
    transaction: TransactionEntry 
    
class BaseLedger:
    def __init__(self, documents, transactional, logger):
        self.documents = documents
        self.transactional = transactional
        self.logger = logger

class BankLedger(BaseLedger):
    def create_account_entry(self, account_entry: AccountEntry):
        # todo ensure account exists
        with self.transactional.get_session() as session:
            statement = select(AccountEntry).where(AccountEntry.account_id == account_entry.account_id and AccountEntry.entity_id == account_entry.entity_id)
            has_account = session.exec(statement).one_or_none()
            print(has_account)
            if has_account:
                raise Exception("Account already exists")
            if account_entry.balance != 0:
                raise Exception("Account initiated with nonzero balance")
            session.add(account_entry)
            session.commit()
            
    def compute_balances(self):
        with self.transactional.get_session() as session:
            statement = select(TransactionEntry).join(AccountEntry, TransactionEntry.account_id == AccountEntry.account_id).where(TransactionEntry.id > AccountEntry.last_transaction_id)
            records = session.exec(statement).all()
            # todo add currency converter service?
            # only allow single currency accounts?
            # allow for multibalance accounts?
            balance = lambda: { t.currency: Decimal(0) for t in records }
            accounts = { t.account_id: balance() for t in records }
            for transaction in records:
                accounts[transaction.account_id][transaction.currency]= accounts[transaction.account_id][transaction.currency] + transaction.amount
            # create a balance_entry_table
            for account_id in accounts.keys():
                balances = accounts[account_id]
                for kb in balances.keys():
                    amount = balances[kb]
                    exists: Optional[BalanceEntry] = session.exec(select(BalanceEntry).where(BalanceEntry.account_id == account_id and BalanceEntry.currency == kb)).one_or_none()
                    
                    if (exists):
                        exists.balance = amount
                        exists.date_updated = datetime.datetime.utcnow()
                        balance_entry = exists
                    else:
                        balance_entry = BalanceEntry(account_id=account_id, balance=amount, currency=kb)
                    
                    session.add(balance_entry)
                    session.commit()
            print("Done")

class EntitiesLedger(BankLedger):
    def get_entity_by_id(self, id: UUID, bucket: str = "bank"):
        couch = self.documents.couch
        db = couch[bucket] if bucket in self.documents.dbs else couch.create(bucket)
        return db.get(str(id))
    
    def get_entities(self, bucket: str = "bank"):
        couch = self.documents.couch
        db = couch[bucket] if bucket in self.documents.dbs else couch.create(bucket)
        docs = db.get("_all_docs")['rows']
        self.logger.warn(docs)
        entities = [db.get(d['id']) for d in docs]
        return entities
    
    def create_account_entity(self, entity: AccountEntity, bucket: str = "bank"):
        couch = self.documents.couch
        db = couch[bucket] if bucket in self.documents.dbs else couch.create(bucket)
        
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
            
            for account in entity.accounts:
                self.create_account_entry(AccountEntry(entity_id=entity.id, account_id=account.id, currency=account.balanceCurrency))
            
        return entity 
    
class TransactionsLedger(BaseLedger):
    def get_transactions(self, offset: int = 0, limit: int = Query(default=100, lte=100)):
        with self.documents.get_session() as session:
            transactions = session.exec(select(TransactionEntry).offset(offset).limit(limit)).all()
            return transactions
        
    def entity_exists(self, session, id):
        entity = session.exec(select(EntityEntry).where(EntityEntry.entity_id == id)).one_or_none()
        return True if entity else False
    
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

class Ledger(EntitiesLedger, TransactionsLedger, BankLedger):
    def __init__(self, documents, transactional, logger):
        super().__init__(documents, transactional, logger)
    
    
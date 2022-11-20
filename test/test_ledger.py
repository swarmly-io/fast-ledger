
from decimal import Decimal
import os
from uuid import uuid4
import pytest
from bank.persistence.database import DocumentDatabase
from bank.persistence.transactional_database import TransactionalDatabase

from bank.ledger.ledger import Ledger
from bank.ledger.ledger_models import AccountEntry, TransactionEntry
from fastapi.logger import logger
from sqlmodel import select

from test.factories import AccountEntryFactory, EntityEntryFactory, TransactionEntryFactory

TEST_BUCKET = "TEST_BUCKET"
    
class TestLedger:
    def setup_method(self):
        self.transactional = TransactionalDatabase("testdb")
        self.documents = DocumentDatabase()
        self.ledger = Ledger(self.documents, self.transactional, logger)
        
    def teardown_method(self):
        os.remove("./testdb.db")

    def test_create_an_account(self):
        entity_uuid, account_uuid,_ = self.make_account()
        result = self.get_account()
        assert result is not None
        assert result.account_id == account_uuid
        assert result.entity_id == entity_uuid

    def make_account(self):
        entity_uuid = uuid4()
        account_uuid = uuid4()

        account_data = { "balance": 0, "currency": "DLRD", "entity_id": str(entity_uuid), "account_id": str(account_uuid), "last_transaction_id": 0 }
        account_entry = AccountEntryFactory.build(**account_data)
        self.ledger.create_account_entry(account_entry)
        return entity_uuid,account_uuid,account_data

    def test_create_a_transaction_plain(self):
        entity_data = { "entity_id": uuid4() }
        entity = EntityEntryFactory.build(**entity_data)
        with self.transactional.get_session() as session:
             session.add(entity)
             session.commit()
        
        _, account_uuid, _ = self.make_account()
        transaction_data = { "account_id": account_uuid, "amount": 5.51, "currency": "DLRD", "transaction_type": "NORMAL", "counter_party_entity_id": entity_data["entity_id"] }
        transaction_entry = TransactionEntryFactory.build(**transaction_data)
        self.ledger.create_transaction(transaction_entry)
        result = self.get_transaction_by_account_id(account_uuid)
        assert result is not None
        assert round(result.amount, 2) == round(Decimal(transaction_data['amount']),2)
        assert result.currency == transaction_data['currency']
        
    def test_create_a_transaction_errors_with_invalid_entity(self):
        with pytest.raises(Exception) as e:       
            _, account_uuid, _ = self.make_account()
            transaction_data = { "account_id": account_uuid, "amount": 5.51, "currency": "DLRD", "transaction_type": "NORMAL", "counter_party_entity_id": uuid4() }
            transaction_entry = TransactionEntryFactory.build(**transaction_data)
            self.ledger.create_transaction(transaction_entry)
                
    def test_create_a_transaction(self):
        account_uuid, transaction_data = self.add_account_create_transaction()
        result = self.get_transaction_by_account_id(account_uuid)

        assert result is not None
        assert round(result.amount, 2) == round(Decimal(transaction_data['amount']),2)
        assert result.currency == transaction_data['currency']

    def add_account_create_transaction(self, transaction_count: int = 1):
        _, account_uuid, _ = self.make_account()
        transaction_data = self.create_transactions(transaction_count, account_uuid)
        return account_uuid,transaction_data

    def create_transactions(self, transaction_count, account_uuid):
        entity_data = { "entity_id": uuid4() }
        for i in range(transaction_count): 
            entity = EntityEntryFactory.build(**entity_data)
            transaction_data = { "account_id": account_uuid, "counter_party_entity_id": None, "amount": 5.51, "currency": "DLRD", "transaction_type": "NORMAL" }
            transaction_entry = TransactionEntryFactory.build(**transaction_data)
            self.ledger.create_transaction(transaction_entry, entity)
        return transaction_data
 
    def get_transaction_by_account_id(self, id):
        with self.transactional.get_session() as session:
            query = select(TransactionEntry).where(TransactionEntry.account_id == id)
            result = session.exec(query).one_or_none()
        print(result)
        return result
    
    def get_account(self):
        with self.transactional.get_session() as session:
            query = select(AccountEntry)
            result = session.exec(query).one_or_none()
        return result

    def test_run_ledger_calculates_correct_balance(self):
        account_uuid, _ = self.add_account_create_transaction(5)
        self.ledger.compute_balances()
        self.create_transactions(5,account_uuid)
        self.ledger.compute_balances()
        with self.transactional.get_session() as session:
            results = session.exec(select(AccountEntry).where(AccountEntry.account_id == account_uuid)).one()
            for balance in results.balances:
                print(balance)
                assert round(balance.balance, 2) == round((Decimal(10) * Decimal(5.51)),2)
                
    def test_get_latest_balance_by_account_gives_correct_balance(self):
        account_uuid, _ = self.add_account_create_transaction(5)
        account_uuid2, _ = self.add_account_create_transaction(1)

        self.ledger.compute_balances()
        self.create_transactions(5,account_uuid)
        balances = self.ledger.get_latest_balance_by_account(account_uuid)
        for currency, balance in balances.items():
                assert round(balance, 2) == round((Decimal(10) * Decimal(5.51)),2)
                
        balances = self.ledger.get_latest_balance_by_account(account_uuid2)
        for currency, balance in balances.items():
                assert round(balance, 2) == round((Decimal(5.51)),2)
        
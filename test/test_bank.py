import datetime
from decimal import Decimal
import random
from uuid import uuid4
from bank.bank_worker import BankWorker
from bank.entity import Account, Entity, Transaction
from bank.query import BankQuery
from bank.utils import first_or_none
from pydantic_factories import ModelFactory
from bank.bank import Bank, Transaction
from devtools import debug

class BankFactory(ModelFactory):
    __model__ = Bank
    
    entities = []
    
class EntityFactory(ModelFactory):
    __model__ = Entity
    
    accounts = []
    
class AccountFactory(ModelFactory):
    __model__ = Account
    
    transactions = []
    
class TransactionFactory(ModelFactory):
    __model__ = Transaction
    
    amount = random.uniform(1.00, 10000.55)
    
class BankOperationsTest:
    pass

class TestBankDetails:
    
    def setup_method(self):
        bank_id = uuid4
        accounts = AccountFactory.batch(size=50)
        account_ids = [a.id for a in accounts]
        for account in accounts:
            external_account_ids = [id for id in account_ids if id != account.id]
            for _ in range(random.randrange(1,20)):
                transaction_data = { "counter_party": random.choice(external_account_ids)  }
                account.transactions.append(TransactionFactory.build(**transaction_data))    
            account.balance = sum(map(lambda x: x.amount, account.transactions))
            if account.balance < 0:
                account.balance = -account.balance + random.uniform(1.0, 1000)
            account.details.bank_id = bank_id
            
        entities = EntityFactory.batch(size = 25)
        for entity in entities:
            entity.accounts.append(accounts.pop())
        
        bank_data = { "entities": entities, "bank_id": bank_id }
        bank = BankFactory.build(**bank_data)
        self.bank_worker = BankWorker(bank)
        self.bank_query = BankQuery(bank)
        
    def test_create_entity(self):
        entity = EntityFactory.build()
        account = AccountFactory.build()
        entity.accounts.append(account)
        
        self.bank_worker.add_entity(entity)
        result = self.bank_query.entity_by_id(entity.id)
        assert entity == result
        
    def test_perform_a_valid_internal_transaction(self):
        accounts = self.bank_query.get_account_list()
        account_from = random.choice(accounts)
        accounts_to = [a for a in accounts if a.id != account_from.id]
        account_to = random.choice(accounts_to)
        
        accounts_from_balance = account_from.balance
        accounts_to_balance = account_to.balance
        
        assert account_from is not None
        assert account_to is not None
        
        amount = account_from.balance * Decimal(0.1)
        trans_name = "invoice 123"
        self.bank_worker.perform_transaction(account_from, account_to, amount, trans_name)
        
        trans_from = first_or_none([t for t in account_from.transactions if t.description == trans_name])
        trans_to = first_or_none([t for t in account_to.transactions if t.description == trans_name])

        assert trans_from is not None
        assert trans_to is not None
        
        assert account_from.balance == accounts_from_balance - amount
        assert account_to.balance == accounts_to_balance + amount 

        t_from = datetime.datetime.utcnow() - trans_from.date
        assert t_from == datetime.timedelta(0)
        
        t_to = datetime.datetime.utcnow() - trans_to.date
        assert t_to == datetime.timedelta(0)

        
                
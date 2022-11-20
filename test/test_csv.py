
import csv
from datetime import datetime
import json
import os
from uuid import uuid4

from faker import Faker
from bank.entities_models import Account
from bank.ledger.ledger_models import AccountEntry, EntityEntry, TransactionEntry
from bank.persistence.database import DocumentDatabase, JSONEncoderExtended

from test.factories import AccountEntityFactory, AccountEntryFactory, EntityEntryFactory, TransactionEntryFactory
import random 

faker = Faker('en-AU')
faker.random.seed(1) 

currencies = ['DLRD', 'NKD', 'BTC', 'HKD']

class RandomTransactionFactory:
    def __init__(self, internal_entity_entries, external_entity_entries, cash_entities, balances):
        self.interal_entity_entries = internal_entity_entries
        self.external_entity_entries = external_entity_entries
        self.cash_entities = cash_entities
        self.balances = balances
        
    def next_entity(self, account_id, entries):
        entity = random.choice(entries)
        if entity.account_id == account_id:
            return self.next_entity(account_id, entries)
        return entity       
    
    def create(self, account_id, first=False):
        def random_currency():
            return random.choice(currencies)
        def random_amount(max_amount):
            return round(random.randint(0, round(max_amount, 0)) + round(random.random(),2), 2)
        
        currency = random_currency()
        current_balance = self.balances[account_id][currency] or 0
        amount = round(random_amount(current_balance) - 1,2)
        if not first and amount < 0:
            print("Fail", current_balance)
            return
        
        print('Amount', amount, current_balance)

        # deposit some money
        def credit_deposit():
            print(random_amount(100000))
            return [TransactionEntry(account_id=account_id, counter_party_entity_id = random.choice(self.cash_entities).id,\
                                    description="cash deposit",\
                                    amount=random_amount(100000), currency=currency,\
                                    transaction_type="DEPOSIT", date=datetime.utcnow()),None]
        
        # perform some transactions with internal entities
        def debit_internal():
            entity = self.next_entity(account_id, self.interal_entity_entries)
            debit = TransactionEntry(account_id=account_id, counter_party_entity_id=entity.id,\
                                        description="Account Transfer Internal", amount=-amount, currency=currency, date=datetime.utcnow(), transaction_type="DEBIT_TRANSFER")
            credit = TransactionEntry(account_id=account_id, counter_party_entity_id=entity.id,\
                                        description="Account Transfer Recieved Internal", amount=amount, currency=currency, date=datetime.utcnow(), transaction_type="CREDIT_TRANSFER")
            return [debit, credit]
        
        # perform some transactions with external entities
        def debit_external():
            entity = self.next_entity(account_id, self.external_entity_entries)
            debit = TransactionEntry(account_id=account_id, counter_party_entity_id=entity.id,\
                                        description="Account Transfer External", amount=-amount, currency=currency, date=datetime.utcnow(), transaction_type="DEBIT_TRANSFER")
            return [debit,None]
        
        # perform some withdrawals
        def debit_withrawal():
            entity = self.next_entity(account_id, self.cash_entities)
            debit = TransactionEntry(account_id=account_id, counter_party_entity_id=entity.id,\
                                        description="Withdrawal", amount=-amount, currency=currency, date=datetime.utcnow(), transaction_type="CASH_WITHDRAWAL")
            return [debit,None]
        
        # todo
        # add an asset
        # add location
        # add valuation
        # trade an asset with another entity
        # trade an asset internally
        if first:
            return credit_deposit()
        else:
            return random.choice([credit_deposit, debit_internal, debit_external, debit_withrawal])()
        
class RandomAssetFactory:
    def __init__(self):
        pass
    
    def create():
        pass
    
    def create_location():
        pass
    
    def create_valuation():
        pass

def create_accounts():
        account_entities = AccountEntityFactory.batch(10)
        account_entries = []
        internal_entities = []
        transaction_entries = []
        for entity in account_entities:
            account_id = uuid4()
            account_data = { "balance": 0, "currency": "DLRD", "entity_id": entity.id, "account_id": account_id, "last_transaction_id": 0 }
            account_entry = AccountEntryFactory.build(**account_data)
            account_entries.append(account_entry)
            account = Account(id=account_id, name=f"{entity.first_name} {entity.last_name}'s Account", details="base ledger", opened_date=datetime.utcnow())
            entity.accounts.append(account)
            
            entity_entry = EntityEntry(first_name=entity.first_name, last_name=entity.last_name, entity_id=entity.id, account_id=account.id)
            internal_entities.append(entity_entry)   
            
        balances = { a.account_id: { c: 0 for c in currencies }  for a in account_entries }      
                        
        external_entity = { "account_id": None, "entity_id": None }
        external_entities = EntityEntryFactory.batch(100, **external_entity)
        
        cash_entity = lambda: { "account_id": None, "entity_id": None, "description": random.choice(["ATM", "SUPERMARKET", "PERSON", "MONEYAPP", "VENDOR"]) }
        cash_entities = [EntityEntryFactory.build(**cash_entity()) for _ in range(20)]
        
        transaction_factory = RandomTransactionFactory(internal_entities, external_entities, cash_entities, balances)
        for a in account_entries:
            initial_transaction, _ = transaction_factory.create(a.account_id, True)
            print(initial_transaction.amount)
            balances[initial_transaction.account_id][initial_transaction.currency] = balances[initial_transaction.account_id][initial_transaction.currency]\
                + initial_transaction.amount         

        for _ in range(100):
          account: AccountEntry = random.choice(account_entries)
          new_transactions = transaction_factory.create(account.account_id)
          if not new_transactions:
              continue
          for t in new_transactions:
              if not t:
                  continue
              
              transaction_entries.append(t)
              print(t)
              balances[t.account_id][t.currency] = balances[t.account_id][t.currency] + t.amount         
              
        entities = internal_entities + external_entities + cash_entities
        
        return account_entities, account_entries, entities, transaction_entries, balances
            
            

def test_test():
    account_entities, account_entries, entities, transaction_entries, balances = create_accounts()
    def dump(entries, name):
        with open(f'test/data/{name}.json', 'w') as f:
            json.dump(list(map(lambda x: DocumentDatabase.todict(x), entries)), f, cls=JSONEncoderExtended, indent=4)
    def dump_dict(d, name):
        with open(f'test/data/{name}.json', 'w') as f:
                json.dump({ str(k): v for k,v in d.items() }, f, cls=JSONEncoderExtended, indent=4)
    
    if not os.path.exists('test/data'):
       os.makedirs('test/data')
    dump(account_entities, "account_entities")
    dump(account_entries, "account_entries")
    dump(entities, "entities")
    dump(transaction_entries, "transaction_entries")
    dump_dict(balances, "balances")
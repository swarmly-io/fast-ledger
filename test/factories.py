
from faker import Faker
from pydantic_factories import ModelFactory, Use
from bank.bank_models import AccountEntity
from bank.ledger.ledger_models import AccountEntry, EntityEntry, TransactionEntry

faker = Faker('en-AU')
faker.random.seed(1)  

class AccountEntityFactory(ModelFactory):
    __model__ = AccountEntity
    
    closed_date = None
    first_name = lambda: faker.first_name()
    last_name = lambda: faker.last_name()
    accounts = []

class AccountEntryFactory(ModelFactory):
    __model__ = AccountEntry
    
class EntityEntryFactory(ModelFactory):
    __model__ = EntityEntry

class TransactionEntryFactory(ModelFactory):
    __model__ = TransactionEntry
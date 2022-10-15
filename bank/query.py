
from uuid import UUID
from bank.utils import first_or_none, flat_map
from bank.bank import Bank

class BankQuery:
    def __init__(self, bank: Bank):
        self.bank = bank
        
    def entity_by_id(self, id: UUID):
        return first_or_none([e for e in self.bank.entities if e.id == id])
    
    def account_by_id(self, id: UUID):
        accounts = flat_map(lambda x: x.accounts, self.bank.entities)
        for account in accounts:
            if account.id == id:
                return account
        return None
    
    def get_account_list(self):
        accounts = list(flat_map(lambda x: x.accounts, self.bank.entities))
        return list(accounts)

        
        

from bank.entity_models import *

class EntityAccountMaintainer:
    def __init__(self, entity: AccountEntity):
        self.entity = entity
        
    def update_name(self, first_name = None, last_name = None):
        if first_name:
            self.entity.first_name = first_name
        if last_name:
            self.entity.last_name = last_name
                
    def update_address(self):
        pass
    
    def add_id_document(self):
        pass
    
    def change_address(self, old: Address, new: Address):
        pass
    
    def add_address(self, new: Address):
        pass
    
    def change_phone(self, old: PhoneNumber, new: PhoneNumber):
        pass
    
    def add_phone(self, new: PhoneNumber):
        pass
    
    def create_account(self, account: Account):
        pass
    
    def close_account(self, account: Account):
        pass
    
    def close_entity(self):
        pass
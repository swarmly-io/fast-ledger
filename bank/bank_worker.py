from datetime import datetime
from decimal import Decimal
from distutils.log import debug
from bank.bank import Bank
from bank.entity import Account, Transaction, Entity
from bank.entity_maintainer import EntityAccountMaintainer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bank.entity import Entity

class BankWorker:
    def __init__(self, bank: Bank):
        self.bank = bank
        
    def add_entity(self, entity: Entity):
        self.bank.entities.append(entity)
            
    def perform_transaction(self, party: Account, counter_party: Account, amount: Decimal, description: str):
        if party.details.bank_id == counter_party.details.bank_id:
            dt = datetime.utcnow()
            from_transaction = Transaction(description = description, amount = amount, counter_party=counter_party.id, date= dt)
            to_transaction = Transaction(description = description, amount = -amount, counter_party=party.id, date= dt)
            new_balance = party.balance - amount
            new_balance_counter_party = counter_party.balance + amount
            if amount >= 0:
                if new_balance >= 0:
                    party.transactions.append(from_transaction)
                    counter_party.transactions.append(to_transaction)
                    
                    party.balance = new_balance
                    counter_party.balance = new_balance_counter_party
                elif new_balance < 0:
                    raise Exception('Insufficient Balance')
            else:
                if new_balance_counter_party >= 0:
                    party.transactions.append(from_transaction)
                    counter_party.transactions.append(to_transaction)
                    
                    party.balance = new_balance
                    counter_party.balance = new_balance_counter_party
                elif new_balance_counter_party < 0:
                    raise Exception('Insufficient Balance')     
    
    def create_statement(self, account: Account):
        pass

    def get_entity_update_interface(self, entity):
        return EntityAccountMaintainer(entity)
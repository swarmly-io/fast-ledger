from datetime import datetime
from decimal import Decimal
from bank.bank.bank import Bank
from bank.bank_models import Account, ReverseApproval, Transaction, AccountEntity
from bank.entity_maintainer import EntityAccountMaintainer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bank.bank_models import AccountEntity

class BankWorker:
    def __init__(self, bank: Bank):
        self.bank = bank
        
    def add_entity(self, entity: AccountEntity):
        self.bank.entities.append(entity)
        
    def deposit(self, account: Account, amount: Decimal):
        if amount <= 0:
            raise Exception("Invalid Deposit Amount")
        
        account.balance += amount    
    
    def withdraw(self, account: Account, amount: Decimal):
        if amount <= 0:
            raise Exception("Invalid Withdrawal Amount")     
        if account.balance < amount:
            raise Exception("Account would be in overdrawn")
        
        account.balance -= amount
            
    def perform_transaction(self, party: Account, counter_party: Account, amount: Decimal, description: str, approval: ReverseApproval = None):
        if party.details.bank_id == counter_party.details.bank_id:
            dt = datetime.utcnow()
            from_transaction = Transaction(description = description, amount = amount, counter_party=counter_party.id, date= dt)
            to_transaction = Transaction(description = description, amount = -amount, counter_party=party.id, date= dt)
            new_balance = party.balance - amount
            new_balance_counter_party = counter_party.balance + amount
            if amount >= 0:
                self.perform_forward_transaction(party, counter_party, from_transaction, to_transaction, new_balance, new_balance_counter_party)
            else:
                self.perform_reversal(party, counter_party, approval, from_transaction, to_transaction, new_balance, new_balance_counter_party) 

    def perform_forward_transaction(self, party, counter_party, from_transaction, to_transaction, new_balance, new_balance_counter_party):
        if new_balance >= 0:
            party.transactions.append(from_transaction)
            counter_party.transactions.append(to_transaction)
                    
            party.balance = new_balance
            counter_party.balance = new_balance_counter_party
        elif new_balance < 0:
            raise Exception('Insufficient Balance')

    def perform_reversal(self, party, counter_party, approval, from_transaction, to_transaction, new_balance, new_balance_counter_party):
        # todo check approvers all have relevant grants
        if not approval or not approval.approved or len(approval.approvers) == 0:
            raise Exception("No approval for reversal")
                
        if new_balance_counter_party >= 0:
            party.transactions.append(from_transaction)
            counter_party.transactions.append(to_transaction)
                    
            party.balance = new_balance
            counter_party.balance = new_balance_counter_party
        elif new_balance_counter_party < 0:
            raise Exception('Insufficient Balance')

    def get_entity_update_interface(self, entity):
        return EntityAccountMaintainer(entity)
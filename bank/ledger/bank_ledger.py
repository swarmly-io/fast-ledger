import datetime
from decimal import Decimal
from typing import Optional
from sqlmodel import select
from bank.ledger.base_ledger import BaseLedger

from bank.ledger.ledger_models import AccountEntry, BalanceEntry, TransactionEntry

class BankLedger(BaseLedger):
    def create_account_entry(self, account_entry: AccountEntry):
        # todo ensure account exists
        with self.transactional.get_session() as session:
            statement = select(AccountEntry).where(AccountEntry.account_id == account_entry.account_id and AccountEntry.entity_id == account_entry.entity_id)
            has_account = session.exec(statement).one_or_none()

            if has_account:
                raise Exception("Account already exists")
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
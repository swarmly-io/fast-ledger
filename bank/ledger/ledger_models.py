
from dataclasses import Field
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import condecimal
from sqlmodel import Field, Relationship, SQLModel

class EntityEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    entity_id: UUID = Field(default_factory=uuid4)
    first_name: Optional[str]
    last_name: Optional[str]
    company_name: Optional[str]
    company_description: Optional[str]
    address: Optional[str]
    account_number: Optional[str]
    bsb: Optional[str]
    account_id: Optional[UUID]
    entity_id: Optional[UUID]

class TransactionEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    account_id: UUID = Field(default=None, foreign_key="accountentry.account_id")
    counter_party_entity_id: Optional[UUID]
    description: Optional[str]
    amount: condecimal(decimal_places=2) = Field(default=0)
    currency: str
    date: datetime = Field(default_factory=datetime.utcnow)
    transaction_type: str
    
class BalanceEntry(SQLModel, table=True):
    id: int = Field(primary_key=True)
    account_id: UUID = Field(foreign_key="accountentry.account_id")
    balance: condecimal(decimal_places=2) = Field(default=0)
    currency: str
    date_updated: datetime = Field(default_factory=datetime.utcnow)

class AccountEntry(SQLModel, table=True):
    id: int = Field(primary_key=True)
    entity_id: UUID
    account_id: UUID
    balances: List['BalanceEntry'] = Relationship()
    last_transaction_id: int = Field(default=0)
    date_updated: datetime = Field(default_factory=datetime.utcnow)
    date_created: datetime = Field(default_factory=datetime.utcnow)
    closed_date: Optional[datetime] = Field(default=None)
    
class AssetEntry(SQLModel, table=True):
    id: int = Field(primary_key=True)
    parent_id: Optional[int]
    asset_id: UUID
    date_updated: datetime = Field(default_factory=datetime.utcnow)
    date_created: datetime = Field(default_factory=datetime.utcnow)
    value: condecimal(decimal_places=2) = Field(default=0)
    value_date: datetime = Field(default_factory=datetime.utcnow)
    valuation_id: Optional[UUID]
    location_id: Optional[UUID]

        
    



    

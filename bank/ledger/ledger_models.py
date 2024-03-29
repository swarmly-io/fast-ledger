
from dataclasses import Field
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import condecimal
from sqlalchemy import BigInteger, Column, Integer
from sqlmodel import Field, Relationship, SQLModel

# todo break this into types
class EntityEntry(SQLModel, table=True):
    id: Optional[int] = Field(sa_column=Column(BigInteger().with_variant(Integer,'sqlite'), primary_key=True, autoincrement=True))
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
    description: Optional[str]

class TransactionEntry(SQLModel, table=True):
    id: Optional[int] = Field(sa_column=Column(BigInteger().with_variant(Integer,'sqlite'), primary_key=True, autoincrement=True))
    account_id: UUID = Field(default=None, foreign_key="accountentry.account_id")
    counter_party_entity_id: Optional[UUID]
    description: Optional[str]
    amount: condecimal(decimal_places=2) = Field(default=0)
    currency: str
    date: datetime = Field(default_factory=datetime.utcnow)
    transaction_type: str
    
class BalanceEntry(SQLModel, table=True):
    id: Optional[int] = Field(sa_column=Column(Integer , primary_key=True, autoincrement=True))
    account_id: UUID = Field(foreign_key="accountentry.account_id")
    balance: condecimal(decimal_places=2) = Field(default=0)
    currency: str
    date_updated: datetime = Field(default_factory=datetime.utcnow)

class AccountEntry(SQLModel, table=True):
    id: Optional[int] = Field(sa_column=Column(BigInteger().with_variant(Integer,'sqlite'), primary_key=True, autoincrement=True))
    entity_id: UUID
    account_id: UUID
    balances: List['BalanceEntry'] = Relationship()
    last_transaction_id: int = Field(default=0)
    date_updated: datetime = Field(default_factory=datetime.utcnow)
    date_created: datetime = Field(default_factory=datetime.utcnow)
    closed_date: Optional[datetime] = Field(default=None)
    
class AssetEntry(SQLModel, table=True):
    id: Optional[int] = Field(sa_column=Column(BigInteger().with_variant(Integer,'sqlite'), primary_key=True, autoincrement=True))
    parent_id: Optional[int]
    asset_id: UUID    
    date_updated: datetime = Field(default_factory=datetime.utcnow)
    date_created: datetime = Field(default_factory=datetime.utcnow)
    # an asset could have multiple currencies and values
    # todo put in valuation table
    value: condecimal(decimal_places=2) = Field(default=0)
    currency: str
    value_date: Optional[datetime] = Field(default=None)
    recent_location_id: Optional[UUID]
    valuation_id: Optional[UUID]

    

        
    



    

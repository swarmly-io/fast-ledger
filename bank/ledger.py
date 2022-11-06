
from dataclasses import Field
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, condecimal
from bank.entity_models import Transaction
from bank.id_basemodel import IdBaseModel

from sqlmodel import Field, SQLModel

class EntityEntry(SQLModel, table=True):
    id: Optional[UUID] = Field(default=None, primary_key=True)
    first_name: Optional[str]
    last_name: Optional[str]
    company_name: Optional[str]
    company_description: Optional[str]
    address: Optional[str]
    account_number: Optional[str]
    bsb: Optional[str]

class TransactionEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    from_id: Optional[UUID]
    to_id: Optional[UUID]
    description: Optional[str]
    amount: condecimal(decimal_places=2) = Field(default=0)
    currency: str
    time_recorded: datetime = Field(default_factory=datetime.utcnow)
    transaction_type: str


    
